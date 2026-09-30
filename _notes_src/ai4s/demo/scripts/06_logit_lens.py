import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from src.config_utils import file_prefix, load_config, output_paths
from src.model_utils import load_causal_lm
from src.hook_utils import get_final_norm
from src.experiment_utils import require_single_token


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--top-k", type=int, default=5)
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    prompt, target_text = cfg.get("prompt"), cfg.get("target_text")
    target_id = require_single_token(tokenizer, target_text)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**inputs, use_cache=False, output_hidden_states=True, return_dict=True)
    norm = get_final_norm(model)
    rows = []
    for layer_idx, h in enumerate(out.hidden_states):
        final_h = h[:, -1, :]
        if norm is not None:
            final_h = norm(final_h)
        logits_lens = model.lm_head(final_h)
        values, ids = torch.topk(logits_lens[0], k=args.top_k)
        rows.append({
            "model_id": cfg["model_id"], "prompt": prompt, "target_text": target_text,
            "layer_index_including_embedding": layer_idx, "target_logit": logits_lens[0, target_id].item(),
            "top_tokens": repr([tokenizer.decode([i.item()]) for i in ids]),
            "top_token_ids": repr([i.item() for i in ids]),
            "top_values": repr([round(v.item(), 4) for v in values]),
        })
        print(rows[-1])
    paths = output_paths(cfg); paths["results"].mkdir(parents=True, exist_ok=True)
    out_path = paths["results"] / f"{file_prefix(cfg)}_logit_lens.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("saved:", out_path)

if __name__ == "__main__":
    main()
