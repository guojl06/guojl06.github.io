import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from src.config_utils import file_prefix, load_config, output_paths
from src.model_utils import load_causal_lm
from src.hook_utils import get_decoder_layers, get_attn_module, get_mlp_module, make_zero_tensor_hook
from src.metrics import next_token_kl, target_logit_drop
from src.experiment_utils import require_single_token


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    return p.parse_args()


def run_ablation(model, inputs, module):
    handle = module.register_forward_hook(make_zero_tensor_hook())
    with torch.no_grad():
        out = model(**inputs, use_cache=False, return_dict=True)
    handle.remove()
    return out


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    prompt, target_text = cfg.get("prompt"), cfg.get("target_text")
    target_id = require_single_token(tokenizer, target_text)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out_base = model(**inputs, use_cache=False, return_dict=True)
    rows = []
    for layer_idx, block in enumerate(get_decoder_layers(model)):
        out_no_attn = run_ablation(model, inputs, get_attn_module(block))
        out_no_mlp = run_ablation(model, inputs, get_mlp_module(block))
        rows += [
            {"model_id": cfg["model_id"], "prompt": prompt, "target_text": target_text, "layer": layer_idx, "intervention": "zero_attention", "kl_base_to_intervened": next_token_kl(out_base.logits, out_no_attn.logits), "target_logit_drop": target_logit_drop(out_base.logits, out_no_attn.logits, target_id)},
            {"model_id": cfg["model_id"], "prompt": prompt, "target_text": target_text, "layer": layer_idx, "intervention": "zero_mlp", "kl_base_to_intervened": next_token_kl(out_base.logits, out_no_mlp.logits), "target_logit_drop": target_logit_drop(out_base.logits, out_no_mlp.logits, target_id)},
        ]
        print(rows[-2]); print(rows[-1])
    paths = output_paths(cfg); paths["results"].mkdir(parents=True, exist_ok=True)
    out_path = paths["results"] / f"{file_prefix(cfg)}_attn_mlp_ablation.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("saved:", out_path)

if __name__ == "__main__":
    main()
