import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import torch
from src.config_utils import load_config
from src.model_utils import load_causal_lm
from src.metrics import topk_tokens


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, cache_dir = load_causal_lm(cfg, args.cache_dir)
    prompt = cfg.get("prompt", "The capital of France is")
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**inputs, use_cache=False, return_dict=True)
    print("model_id:", cfg["model_id"])
    print("device:", device)
    print("cache_dir:", cache_dir or "default")
    print("prompt:", repr(prompt))
    print("logits:", tuple(out.logits.shape))
    print("top tokens:")
    for tok, val, idx in topk_tokens(tokenizer, out.logits, k=10):
        print(f"  {idx:>8} {tok!r:<16} {val:.4f}")

if __name__ == "__main__":
    main()
