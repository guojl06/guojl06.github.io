import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from tqdm import tqdm

from src.config_utils import file_prefix, load_config, output_paths
from src.experiment_utils import require_single_token
from src.hook_utils import get_decoder_layers, make_skip_block_hook
from src.metrics import next_token_kl, target_logit_drop, top1_token
from src.model_utils import load_causal_lm
from src.prompt_utils import prompt_suite_from_config, row_tags_json, row_variables_json, validate_prompt_rows


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--prompt-suite", default=None)
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--max-examples", type=int, default=None)
    p.add_argument("--skip-invalid", action="store_true")
    p.add_argument("--out", default=None)
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    rows_in = prompt_suite_from_config(cfg, args.prompt_suite, args.max_examples)
    errors = validate_prompt_rows(rows_in, tokenizer=tokenizer, max_prompt_tokens=cfg.get("experiments", {}).get("global_defaults", {}).get("max_prompt_tokens"))
    if errors and not args.skip_invalid:
        raise ValueError("Prompt validation failed. Use scripts/11_validate_prompt_suite.py or pass --skip-invalid.")
    bad_ids = {e.get("prompt_id") for e in errors}
    layers = get_decoder_layers(model)
    rows_out = []
    for row in tqdm(rows_in, desc="prompts"):
        if args.skip_invalid and row.get("prompt_id") in bad_ids:
            continue
        if row.get("task") == "activation_patching":
            continue
        target_id = require_single_token(tokenizer, row["target_text"])
        inputs = tokenizer(row["prompt"], return_tensors="pt").to(device)
        with torch.no_grad():
            out_base = model(**inputs, use_cache=False, return_dict=True)
        top1_base = top1_token(tokenizer, out_base.logits)
        for layer_idx, layer in enumerate(layers):
            handle = layer.register_forward_hook(make_skip_block_hook())
            with torch.no_grad():
                out_skip = model(**inputs, use_cache=False, return_dict=True)
            handle.remove()
            top1_int = top1_token(tokenizer, out_skip.logits)
            rows_out.append({
                "model_id": cfg["model_id"], "prompt_id": row.get("prompt_id"), "task": row.get("task"), "condition": row.get("condition"),
                "intervention": "skip_block", "layer": layer_idx, "target_text": row.get("target_text"),
                "kl_base_to_intervened": next_token_kl(out_base.logits, out_skip.logits),
                "target_logit_drop": target_logit_drop(out_base.logits, out_skip.logits, target_id),
                "top1_base": top1_base, "top1_intervened": top1_int, "top1_change": top1_base != top1_int,
                "variables_json": row_variables_json(row), "tags_json": row_tags_json(row),
            })
    paths = output_paths(cfg); paths["results"].mkdir(parents=True, exist_ok=True)
    out_path = Path(args.out) if args.out else paths["results"] / f"{file_prefix(cfg)}_batch_layer_skip.csv"
    pd.DataFrame(rows_out).to_csv(out_path, index=False)
    print("saved:", out_path)

if __name__ == "__main__":
    main()
