from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .config_utils import configure_hf_cache_env, resolve_cache_dir


def get_device(requested: str = "auto") -> str:
    requested = (requested or "auto").lower()
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def get_dtype(requested: str = "auto", device: str = "cpu"):
    requested = requested or "auto"
    if requested != "auto":
        mapping = {
            "float32": torch.float32,
            "fp32": torch.float32,
            "float16": torch.float16,
            "fp16": torch.float16,
            "bfloat16": torch.bfloat16,
            "bf16": torch.bfloat16,
        }
        if requested not in mapping:
            raise ValueError(f"Unsupported dtype: {requested}")
        return mapping[requested]
    if device in {"cuda", "mps"}:
        return torch.float16
    return torch.float32


def load_tokenizer(cfg: Dict[str, Any], cache_dir_override: Optional[str] = None):
    cache_dir = resolve_cache_dir(cfg, cache_dir_override)
    configure_hf_cache_env(cache_dir)
    trust = bool(cfg.get("model", {}).get("trust_remote_code", cfg.get("runtime", {}).get("trust_remote_code", cfg.get("trust_remote_code", False))))
    local_files_only = bool(cfg.get("local_files_only", cfg.get("runtime", {}).get("local_files_only", False)))
    tokenizer = AutoTokenizer.from_pretrained(
        cfg["model_id"],
        cache_dir=cache_dir,
        trust_remote_code=trust,
        local_files_only=local_files_only,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(tokenizer, "eos_token", None) is not None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def load_causal_lm(cfg: Dict[str, Any], cache_dir_override: Optional[str] = None):
    cache_dir = resolve_cache_dir(cfg, cache_dir_override)
    configure_hf_cache_env(cache_dir)
    device = get_device(cfg.get("device") or cfg.get("runtime", {}).get("device", "auto"))
    dtype = get_dtype(cfg.get("dtype") or cfg.get("runtime", {}).get("dtype", "auto"), device)
    trust = bool(cfg.get("model", {}).get("trust_remote_code", cfg.get("runtime", {}).get("trust_remote_code", cfg.get("trust_remote_code", False))))
    local_files_only = bool(cfg.get("local_files_only", cfg.get("runtime", {}).get("local_files_only", False)))
    attn_impl = cfg.get("attn_implementation") or cfg.get("runtime", {}).get("attn_implementation", "eager")
    low_cpu_mem_usage = bool(cfg.get("runtime", {}).get("low_cpu_mem_usage", True))

    tokenizer = AutoTokenizer.from_pretrained(
        cfg["model_id"],
        cache_dir=cache_dir,
        trust_remote_code=trust,
        local_files_only=local_files_only,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(tokenizer, "eos_token", None) is not None:
        tokenizer.pad_token = tokenizer.eos_token

    kwargs: Dict[str, Any] = {
        "torch_dtype": dtype,
        "cache_dir": cache_dir,
        "trust_remote_code": trust,
        "local_files_only": local_files_only,
        "low_cpu_mem_usage": low_cpu_mem_usage,
    }
    if attn_impl:
        kwargs["attn_implementation"] = attn_impl

    try:
        model = AutoModelForCausalLM.from_pretrained(cfg["model_id"], **kwargs)
    except TypeError:
        kwargs.pop("attn_implementation", None)
        model = AutoModelForCausalLM.from_pretrained(cfg["model_id"], **kwargs)

    model = model.to(device)
    model.eval()
    return model, tokenizer, device, cache_dir


def encode(tokenizer, text: str, device: str):
    return tokenizer(text, return_tensors="pt").to(device)


def token_ids(tokenizer, text: str) -> list[int]:
    return tokenizer.encode(text, add_special_tokens=False)
