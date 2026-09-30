#!/usr/bin/env python3
"""demo-server: OpenAI 兼容 API + activation hook (多模型自动切换版).

PsyST Lab 当普通 API 连. 请求体里的 `model` 字段决定加载哪个模型:
  - 当前已加载该模型 → 直接复用
  - 请求的是别的模型 → 卸载当前模型 (去hook + del + empty_cache),
    加载请求的模型 (~4s), 再服务

同一时刻只有一个模型在显存里 (16G 放不下两个). 整个请求加锁,
保证两个不同模型的请求不会互相把对方卸掉.

行为: 模型生成文本返回 (PsyST Lab exact match 评分)
机制: 每层 decoder block 输出 hook → 查询位置逐层残差 + (可选) attention,
      存 outputs/activations/<id>.pt; .pt 里记 model_id, 方便后续
      logit-lens 知道用哪个模型的 lm_head/norm 投影.

用法:
  python server.py --cache-dir ./hf_cache --port 8000
  python server.py --model-id Qwen/Qwen3.5-2B --cache-dir ./hf_cache --port 8000
  python server.py --no-preload --cache-dir ./hf_cache --port 8000   # 首请求再加载
"""
from __future__ import annotations
import argparse
import gc
import re
import threading
import time
import uuid
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    import uvicorn
    HAVE_FASTAPI = True
except ImportError:
    HAVE_FASTAPI = False


# ===========================================================================
# 模型注册表: alias → canonical HF id
# ===========================================================================
# 已下载到 ./hf_cache 的模型. thinking 字段:
#   "qwen" → chat template 支持 enable_thinking (Qwen3 / Qwen3.5), 默认关
#   "none" → 标准 instruct, 无 thinking 机制 (Qwen3-2507 / Phi / Llama / SmolLM)
# 注意: 实际是否支持 enable_thinking 在加载时再探测一次 chat_template, 这里只是默认意图.
MODELS: list[dict] = [
    {"id": "Qwen/Qwen3.5-2B",               "aliases": ["qwen3.5-2b"],                                           "thinking": "qwen"},
    {"id": "Qwen/Qwen3.5-0.8B",             "aliases": ["qwen3.5-0.8b"],                                         "thinking": "qwen"},
    {"id": "Qwen/Qwen3-4B-Instruct-2507",   "aliases": ["qwen3-4b-instruct-2507", "qwen3-4b-2507"],              "thinking": "none"},
    {"id": "HuggingFaceTB/SmolLM3-3B",      "aliases": ["smollm3-3b", "smollm3"],                                "thinking": "none"},
    {"id": "microsoft/Phi-3.5-mini-instruct", "aliases": ["phi-3.5-mini", "phi3.5-mini"],                        "thinking": "none"},
    {"id": "unsloth/Llama-3.2-3B-Instruct", "aliases": ["llama-3.2-3b", "llama3.2-3b", "llama-3.2-3b-instruct"], "thinking": "none"},
]

# alias / full-id / 末段 → canonical id (全小写匹配)
_ALIAS2ID: dict[str, str] = {}
for _m in MODELS:
    _ALIAS2ID[_m["id"].lower()] = _m["id"]
    _ALIAS2ID[_m["id"].split("/")[-1].lower()] = _m["id"]
    for _a in _m["aliases"]:
        _ALIAS2ID[_a.lower()] = _m["id"]


def resolve_model_id(name: str) -> str | None:
    """请求里的 model 名字 → canonical HF id. 认不出返回 None."""
    if not name:
        return None
    return _ALIAS2ID.get(name.lower().strip())


# 激活存档目录: 锚定脚本所在目录, 不依赖 CWD (修掉"重启换目录→找不到旧.pt")
ACTIVATIONS_DIR = Path(__file__).resolve().parent / "outputs" / "activations"


# ===========================================================================
# HookedModel: 单个模型的加载 + hook + chat
# ===========================================================================
class HookedModel:
    """加载一个模型, 注册每层 hook, 提供 chat (生成 + 存 activation)."""

    def __init__(self, model_id: str, cache_dir: str | None, device: str = "auto",
                 dtype: str = "auto", enable_thinking: bool = False, attn_impl: str = "sdpa"):
        self.model_id = model_id
        self.cache_dir = cache_dir
        self.enable_thinking = enable_thinking

        print(f"[load] {model_id} from {cache_dir or 'default'}...", flush=True)
        dtype_map = {"auto": None, "fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}
        dt = dtype_map.get(dtype)

        # 优先走 transformers 内置类 (官方维护, 跟版本同步, 不受 remote code 陈旧拖累);
        # 内置不支持该架构时回退 trust_remote_code=True (会下载模型仓库自带的 modeling 代码).
        base = {"low_cpu_mem_usage": True, "device_map": "auto",
                "local_files_only": True, "attn_implementation": attn_impl}
        if dt:
            base["torch_dtype"] = dt
        if cache_dir:
            base["cache_dir"] = cache_dir

        last_err: Exception | None = None
        for trc in (False, True):
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id, trust_remote_code=trc, local_files_only=True, cache_dir=cache_dir)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id, trust_remote_code=trc, **base)
                print(f"[load] via trust_remote_code={trc} ({'内置类' if not trc else 'remote code'})",
                      flush=True)
                break
            except Exception as e:
                last_err = e
                print(f"[load] trust_remote_code={trc} 失败: {type(e).__name__}: {str(e)[:120]}",
                      flush=True)
        else:
            raise last_err

        self.device = "cuda" if (device == "cuda" or (device == "auto" and torch.cuda.is_available())) else "cpu"
        self.model.eval()

        # 探测 chat_template 是否支持 enable_thinking (Qwen3/3.5 支持, 其它一般不支持)
        try:
            tmpl = self.tokenizer.chat_template or ""
            self.supports_enable_thinking = "enable_thinking" in tmpl
        except Exception:
            self.supports_enable_thinking = False

        self._hooks: list = []
        self._current_cache: dict[str, torch.Tensor] = {}
        self._last_attentions: list = []
        self._register_hooks()
        print(f"[load] done. device={self.device}, layers={self.num_layers}, "
              f"enable_thinking_supported={self.supports_enable_thinking}", flush=True)

    @property
    def num_layers(self) -> int:
        return len(self.model.model.layers)

    def _register_hooks(self):
        """每层 decoder block 输出 hook → _current_cache[layer_i] = 整层输出."""
        def make_hook(layer_idx):
            def hook(module, inp, out):
                h = out[0] if isinstance(out, tuple) else out
                self._current_cache[f"layer_{layer_idx}"] = h.detach().cpu()
            return hook
        for i, layer in enumerate(self.model.model.layers):
            self._hooks.append(layer.register_forward_hook(make_hook(i)))

    def unload(self):
        """卸载: 去 hook, 删模型/tokenizer, 清显存. 给 ModelManager 换模型用."""
        for h in self._hooks:
            try:
                h.remove()
            except Exception:
                pass
        self._hooks.clear()
        self._current_cache.clear()
        self._last_attentions.clear()
        try:
            del self.model
            del self.tokenizer
        except Exception:
            pass
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print(f"[unload] {self.model_id} freed", flush=True)

    def chat(self, messages: list[dict], temperature: float = 0.0, max_tokens: int = 512,
             need_attention: bool = True, chat_template_kwargs: dict | None = None) -> dict:
        """生成回复 + 存 activation. 返回 {content, input_tokens, output_tokens, activation_id, ...}."""
        # thinking 控制: 支持 enable_thinking 的模型默认关 (实验要确定性短回答)
        ctk = dict(chat_template_kwargs or {})
        if self.supports_enable_thinking and "enable_thinking" not in ctk:
            ctk["enable_thinking"] = self.enable_thinking
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, **ctk)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        input_len = inputs["input_ids"].shape[1]
        self._current_cache = {}
        self._last_attentions = []

        # generate 不开 attention (省显存), 只生成文本
        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
                return_dict_in_generate=True,
            )
        new_tokens = out.sequences[0][input_len:]
        full_seq = out.sequences[0]
        del out
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # 要 attention: 单独 forward 一次 (只存一次, 不爆显存)
        if need_attention:
            with torch.no_grad():
                fwd = self.model(full_seq.unsqueeze(0).to(self.device), output_attentions=True)
                # attentions: tuple of (1, n_heads, seq, seq) per layer
                self._last_attentions = [a[0].cpu() for a in fwd.attentions]
            del fwd
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        content = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        # 去掉 think 标签: 空 <think></think> 和带内容的 <think>...</think> 都去
        content = re.sub(r"<think>.*?</think>\s*", "", content, flags=re.DOTALL).strip()
        act_info = self._save_activation(input_len, messages, content)
        return {"content": content, "input_tokens": input_len,
                "output_tokens": new_tokens.shape[0], **act_info}

    def _save_activation(self, input_len: int, messages: list[dict], content: str) -> dict:
        """存 activation + attention 到 .pt, 返回 {activation_id, activation_path}."""
        activation_id = f"act_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        ACTIVATIONS_DIR.mkdir(parents=True, exist_ok=True)
        act_path = ACTIVATIONS_DIR / f"{activation_id}.pt"
        query_act = {k: v[0, -1, :].clone() for k, v in self._current_cache.items()}
        attention_saved: dict = {}
        if self._last_attentions:
            for lidx, attn in enumerate(self._last_attentions):
                if attn is not None:
                    attention_saved[f"layer_{lidx}"] = attn[0].detach().cpu()  # (n_heads, seq, seq)
        torch.save({
            "activation_id": activation_id,
            "model_id": self.model_id,           # ← 多模型必须记: logit-lens 要知道用谁的 lm_head
            "input_len": input_len,
            "num_layers": self.num_layers,
            "activations": query_act,
            "attentions": attention_saved if attention_saved else None,
            "messages": messages, "response": content, "timestamp": time.time(),
        }, act_path)
        return {"activation_id": activation_id, "activation_path": str(act_path)}


# ===========================================================================
# ModelManager: 持有当前唯一模型, 按请求切换
# ===========================================================================
class ModelManager:
    """同一时刻只挂一个模型; 请求的 model 不同就卸载重载. 整个 chat 加锁."""

    def __init__(self, cache_dir: str, device: str = "auto", dtype: str = "auto",
                 default_enable_thinking: bool = False, attn_impl: str = "sdpa"):
        self.cache_dir = cache_dir if cache_dir != "auto" else None
        self.device = device
        self.dtype = dtype
        self.default_enable_thinking = default_enable_thinking
        self.attn_impl = attn_impl
        self.current: HookedModel | None = None
        self._lock = threading.Lock()

    def _ensure_loaded_locked(self, model_id: str) -> HookedModel:
        """调用方已持锁. 不同则换."""
        if self.current is not None and self.current.model_id == model_id:
            return self.current
        if self.current is not None:
            self.current.unload()
            self.current = None
        self.current = HookedModel(
            model_id=model_id, cache_dir=self.cache_dir,
            device=self.device, dtype=self.dtype,
            enable_thinking=self.default_enable_thinking,
            attn_impl=self.attn_impl,
        )
        return self.current

    def ensure_loaded(self, model_id: str) -> HookedModel:
        """加载指定模型 (若未加载). 给 /health 或预热用."""
        with self._lock:
            return self._ensure_loaded_locked(model_id)

    def handle_chat(self, model_id: str, messages: list[dict], **chat_kwargs) -> dict:
        """加锁完成 切换(按需) + chat. 两个不同模型的请求会被串行化."""
        with self._lock:
            hm = self._ensure_loaded_locked(model_id)
            return hm.chat(messages, **chat_kwargs)

    # ---- 机制端点: 只读 .pt, 不依赖当前加载的模型 ----
    def get_mechanism(self, activation_id: str) -> dict:
        p = ACTIVATIONS_DIR / f"{activation_id}.pt"
        if not p.exists():
            return {"error": "not found"}
        data = torch.load(p, map_location="cpu", weights_only=False)

        layers = []
        for k in sorted(data["activations"].keys(), key=lambda x: int(x.split("_")[1])):
            v = data["activations"][k]
            layers.append({
                "layer": int(k.split("_")[1]),
                "norm": round(float(v.norm().item()), 4),
                "mean": round(float(v.mean().item()), 4),
            })

        heads = []
        attns = data.get("attentions") or {}
        for k in sorted(attns.keys(), key=lambda x: int(x.split("_")[1])):
            a = attns[k]  # (n_heads, seq, seq)
            lidx = int(k.split("_")[1])
            last_attn = a[:, -1, :]  # (n_heads, seq)
            for hi in range(a.shape[0]):
                w = last_attn[hi]
                w = w / (w.sum() + 1e-12)
                entropy = float(-(w * (w + 1e-12).log()).sum())
                heads.append({
                    "layer": lidx, "head": hi,
                    "entropy": round(entropy, 4),
                    "max_pos": int(w.argmax()), "max_val": round(float(w.max()), 4),
                })

        return {
            "activation_id": activation_id,
            "model_id": data.get("model_id", "?"),
            "num_layers": data["num_layers"],
            "input_tokens": data["input_len"],
            "response": data.get("response", "")[:200],
            "layers": layers,
            "heads": heads,
        }

    def compare_mechanism(self, id_a: str, id_b: str) -> dict:
        pa = ACTIVATIONS_DIR / f"{id_a}.pt"
        pb = ACTIVATIONS_DIR / f"{id_b}.pt"
        if not pa.exists() or not pb.exists():
            return {"error": "one or both not found"}
        da = torch.load(pa, map_location="cpu", weights_only=False)
        db = torch.load(pb, map_location="cpu", weights_only=False)

        # 层数可能不同 (跨模型对比), 取两边都有的层
        keys_a = set(da["activations"].keys())
        keys_b = set(db["activations"].keys())
        common = sorted(keys_a & keys_b, key=lambda x: int(x.split("_")[1]))
        diffs = []
        for k in common:
            va, vb = da["activations"][k], db["activations"][k]
            if va.shape != vb.shape:
                continue  # 维度不同跳过
            diffs.append({
                "layer": int(k.split("_")[1]),
                "diff_norm": round(float((va - vb).norm().item()), 4),
                "a_norm": round(float(va.norm().item()), 4),
                "b_norm": round(float(vb.norm().item()), 4),
            })
        return {
            "id_a": id_a, "model_a": da.get("model_id", "?"), "response_a": da.get("response", "")[:200],
            "id_b": id_b, "model_b": db.get("model_id", "?"), "response_b": db.get("response", "")[:200],
            "diffs": diffs,
        }


# ===========================================================================
# FastAPI app
# ===========================================================================
def build_app(mgr: ModelManager) -> "FastAPI":
    app = FastAPI(title="demo-server (multi-model)")

    @app.get("/v1/models")
    async def list_models():
        return {"object": "list", "data": [
            {"id": m["id"], "aliases": m["aliases"],
             "loaded": (mgr.current is not None and mgr.current.model_id == m["id"])}
            for m in MODELS
        ]}

    @app.post("/v1/chat/completions")
    async def chat_completions(request: Request):
        body = await request.json()
        requested = body.get("model", "")
        model_id = resolve_model_id(requested)
        if model_id is None:
            return JSONResponse(
                {"error": f"unknown model: {requested!r}",
                 "available": [m["id"] for m in MODELS]},
                status_code=400)

        messages = body.get("messages", [])
        temperature = body.get("temperature", 0.0)
        max_tokens = body.get("max_tokens", 512)
        ctk = (body.get("chat_template_kwargs")
               or body.get("extra_body", {}).get("chat_template_kwargs"))
        need_attn = body.get("need_attention", False)

        try:
            result = mgr.handle_chat(
                model_id, messages,
                temperature=temperature, max_tokens=max_tokens,
                need_attention=need_attn, chat_template_kwargs=ctk,
            )
        except Exception as e:
            return JSONResponse({"error": f"load/infer failed for {model_id}: {e}"},
                                status_code=500)

        return JSONResponse({
            "id": f"chatcmpl-{result['activation_id']}",
            "object": "chat.completion",
            "model": model_id,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": result["content"]},
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": result["input_tokens"],
                "completion_tokens": result["output_tokens"],
                "total_tokens": result["input_tokens"] + result["output_tokens"],
            },
            "x_activation_id": result["activation_id"],
            "x_activation_path": result["activation_path"],
            "x_model_loaded": model_id,
        })

    @app.get("/mechanism/{activation_id}")
    async def mechanism(activation_id: str):
        return mgr.get_mechanism(activation_id)

    @app.get("/mechanism/compare")
    async def mechanism_compare(a: str = "", b: str = ""):
        return mgr.compare_mechanism(a, b)

    @app.get("/health")
    async def health():
        return {"status": "ok",
                "current_model": mgr.current.model_id if mgr.current else None,
                "available_models": [m["id"] for m in MODELS]}

    return app


# ===========================================================================
# main
# ===========================================================================
def main():
    ap = argparse.ArgumentParser(description="demo-server (multi-model): 请求里指定 model 自动切换")
    ap.add_argument("--model-id", default="Qwen/Qwen3.5-2B",
                    help="启动时预加载的模型 (可用 alias, 如 qwen3.5-0.8b)")
    ap.add_argument("--cache-dir", default="./hf_cache")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--device", default="auto")
    ap.add_argument("--dtype", default="auto")
    ap.add_argument("--attn", default="sdpa", choices=["sdpa", "eager", "flash_attention_2"],
                    help="attention 实现: sdpa=快/默认/不返回权重(行为sweep用); eager=慢/可抓attention权重(机制分析用)")
    ap.add_argument("--enable-thinking", action="store_true", help="默认关 thinking; 加此开关才开")
    ap.add_argument("--no-preload", action="store_true", help="不在启动时加载, 等首个请求再加载")
    args = ap.parse_args()

    mgr = ModelManager(
        cache_dir=args.cache_dir, device=args.device, dtype=args.dtype,
        default_enable_thinking=args.enable_thinking, attn_impl=args.attn,
    )

    if not args.no_preload:
        mid = resolve_model_id(args.model_id) or args.model_id
        print(f"[init] preloading {mid} ...", flush=True)
        mgr.ensure_loaded(mid)

    if not HAVE_FASTAPI:
        print("[error] fastapi 未装. pip install fastapi uvicorn")
        return

    app = build_app(mgr)
    print(f"[serve] http://{args.host}:{args.port}  "
          f"(thinking={'on' if args.enable_thinking else 'off'}, "
          f"models={[m['id'] for m in MODELS]})", flush=True)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
