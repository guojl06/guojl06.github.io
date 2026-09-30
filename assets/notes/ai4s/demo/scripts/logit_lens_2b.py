#!/usr/bin/env python3
"""Logit-lens on Qwen3.5-2B PI Release (查询位置, CPU+SDPA, 不打扰 GPU sweep).

对 G0/G8s × u97 (可配) 的 trials:
  1. 从 results.jsonl 拿 activation_id → 加载 .pt → 取 messages(prompt)
  2. 解析 prompt 流: 每 key 的 first(旧值)/target(新值=最后出现)
  3. 重新 forward 输入 prompt (output_hidden_states) → 取查询位置(最后输入token)逐层残差
  4. 每层残差 → final_norm → lm_head → 读 target/old 首 token logit → margin
  5. 聚合 G0 vs G8s → mean margin(ℓ) ± sem, 存 JSON

用法:
  python logit_lens_2b.py <results.jsonl> <cond1,cond2> <max_trials> <out.json>
"""
import sys, json, re, time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

AD = "/home/st/local_llm_research_v2/outputs/activations"
MODEL = "Qwen/Qwen3.5-2B"
CACHE = "/home/st/local_llm_research_v2/hf_cache"

RESULTS = sys.argv[1] if len(sys.argv) > 1 else "results_2b_batch1.jsonl"
CONDS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["G0_u97_p2.5", "G8s_u97_p2.5"]
MAXT = int(sys.argv[3]) if len(sys.argv) > 3 else 10
OUT = sys.argv[4] if len(sys.argv) > 4 else "/home/st/local_llm_research_v2/logit_lens_2b_u97.json"

print(f"[cfg] model={MODEL} conds={CONDS} max_trials/cond={MAXT}", flush=True)
print("[load] model on CPU (sdpa, fp32)...", flush=True)
tok = AutoTokenizer.from_pretrained(MODEL, cache_dir=CACHE, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL, cache_dir=CACHE, local_files_only=True,
    torch_dtype=torch.float32, device_map="cpu", attn_implementation="sdpa")
model.eval()
final_norm = model.model.norm
lm_head = model.lm_head
NLAYERS = model.config.num_hidden_layers
print(f"[load] done. layers={NLAYERS}, vocab={lm_head.out_features}", flush=True)


def parse_stream(prompt):
    """从 prompt 解析每 key 的 first(旧值) 和 target(最后值)."""
    m1 = prompt.find("The text stream starts on the next line.")
    m2 = prompt.find("What are the current value")
    stream = prompt[m1:m2] if m1 >= 0 and m2 >= 0 else prompt
    mk = re.search(r"track include (.+?)\.", prompt)
    keys = [k.strip() for k in mk.group(1).split(",")] if mk else []
    first, last = {}, {}
    for pair in stream.split(";"):
        if ":" not in pair:
            continue
        k, _, v = pair.partition(":")
        k, v = k.strip(), v.strip()
        if not k or not v:
            continue
        if k not in first:
            first[k] = v
        last[k] = v
    keys = [k for k in keys if k in first and k in last and first[k] != last[k]]
    return keys, first, last


def first_tok(val):
    """value 在 'is <value>' 上下文里的首 token id (带前导空格)."""
    ids = tok.encode(" " + val, add_special_tokens=False)
    return ids[0] if ids else None


@torch.no_grad()
def query_logits_per_layer(prompt):
    """forward prompt → 查询位置(最后输入token)逐层 logits (经 final_norm+lm_head)."""
    text = tok.apply_chat_template(
        [{"role": "user", "content": prompt}],
        tokenize=False, add_generation_prompt=True, enable_thinking=False)
    enc = tok(text, return_tensors="pt")
    out = model(**enc, output_hidden_states=True)
    # hidden_states: [0]=embedding 输入, [1..L]=各 block 输出 (即残差)
    per_layer = []
    for hs in out.hidden_states[1:]:            # 每层 block 输出
        r = hs[0, -1, :]                          # 查询位置残差 (d,)
        logits = lm_head(final_norm(r)).float()   # (vocab,)
        per_layer.append(logits)
    del out
    return per_layer


# 收集 trials
by_cond = {c: [] for c in CONDS}
with open(RESULTS) as f:
    for line in f:
        r = json.loads(line)
        cid = r["condition_id"]
        if cid in by_cond and len(by_cond[cid]) < MAXT:
            by_cond[cid].append(r)

results = {}
for cid in CONDS:
    trials = by_cond[cid]
    print(f"\n=== {cid}: {len(trials)} trials ===", flush=True)
    results[cid] = []
    for r in trials:
        aid = r["raw"]["activation_id"]
        pt = torch.load(f"{AD}/{aid}.pt", map_location="cpu", weights_only=False)
        prompt = pt["messages"][0]["content"]
        keys, first, last = parse_stream(prompt)
        tgt_t = {k: first_tok(last[k]) for k in keys}
        fst_t = {k: first_tok(first[k]) for k in keys}
        keys = [k for k in keys if tgt_t.get(k) is not None and fst_t.get(k) is not None]
        t0 = time.time()
        per_layer = query_logits_per_layer(prompt)
        margins = []
        for logits in per_layer:
            ms = [(logits[tgt_t[k]] - logits[fst_t[k]]).item() for k in keys]
            margins.append(sum(ms) / len(ms))
        results[cid].append({
            "trial": r["trial"], "accuracy": r["scores"].get("accuracy"),
            "n_keys": len(keys), "margins": margins})
        print(f"  trial {r['trial']}: acc={r['scores'].get('accuracy'):.2f} "
              f"nkeys={len(keys)} {time.time()-t0:.0f}s", flush=True)

# 聚合
agg = {}
for cid, rs in results.items():
    if not rs:
        continue
    M = np.array([x["margins"] for x in rs])    # (n_trials, n_layers)
    agg[cid] = {
        "mean": M.mean(0).tolist(), "sem": (M.std(0) / np.sqrt(len(rs))).tolist(),
        "n_trials": len(rs), "n_keys_avg": float(np.mean([x["n_keys"] for x in rs])),
        "accuracy_avg": float(np.mean([x["accuracy"] for x in rs])),
    }

json.dump({"model": MODEL, "n_layers": NLAYERS, "conditions": results, "agg": agg},
          open(OUT, "w"), indent=2)
print(f"\n[done] saved {OUT}", flush=True)
print("[agg] per-condition mean margin @ last layer / @ mid layer:")
for cid, a in agg.items():
    print(f"  {cid}: L{NLAYERS//2}={a['mean'][NLAYERS//2]:+.3f}  L{NLAYERS-1}={a['mean'][-1]:+.3f}  "
          f"(acc={a['accuracy_avg']:.2f})")
