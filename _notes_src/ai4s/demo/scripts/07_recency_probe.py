import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from src.config_utils import file_prefix, load_config, output_paths
from src.model_utils import load_causal_lm
from src.metrics import target_logit, topk_tokens
from src.experiment_utils import require_single_token


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    rec = cfg.get("prompts", {}).get("recency_probe", {})
    target_text = rec.get("target_text", " red")
    target_id = require_single_token(tokenizer, target_text)
    rows = []
    for item in rec.get("conditions", []):
        inputs = tokenizer(item["prompt"], return_tensors="pt").to(device)
        with torch.no_grad():
            out = model(**inputs, use_cache=False, return_dict=True)
        row = {"model_id": cfg["model_id"], "condition": item["name"], "prompt": item["prompt"], "target_text": target_text, "target_logit": target_logit(out.logits, target_id), "top5_tokens": repr([(t, round(v,3)) for t,v,_ in topk_tokens(tokenizer, out.logits, k=5)]), "num_tokens": inputs["input_ids"].shape[1]}
        rows.append(row); print(row)
    paths = output_paths(cfg); paths["results"].mkdir(parents=True, exist_ok=True)
    out_path = paths["results"] / f"{file_prefix(cfg)}_recency_probe.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("saved:", out_path)

if __name__ == "__main__":
    main()
