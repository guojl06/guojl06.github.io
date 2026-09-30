import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from src.config_utils import file_prefix, load_config, output_paths
from src.model_utils import load_causal_lm
from src.hook_utils import get_decoder_layers, hidden_from_output, replace_hidden_in_output
from src.metrics import target_logit
from src.experiment_utils import require_single_token


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--clean-prompt", default=None)
    p.add_argument("--corrupt-prompt", default=None)
    p.add_argument("--target-text", default=None)
    p.add_argument("--patch-position", type=int, default=-1)
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    clean_prompt = args.clean_prompt or cfg.get("clean_prompt")
    corrupt_prompt = args.corrupt_prompt or cfg.get("corrupt_prompt")
    target_text = args.target_text or cfg.get("target_text")
    target_id = require_single_token(tokenizer, target_text)
    clean_inputs = tokenizer(clean_prompt, return_tensors="pt").to(device)
    corrupt_inputs = tokenizer(corrupt_prompt, return_tensors="pt").to(device)
    if clean_inputs["input_ids"].shape != corrupt_inputs["input_ids"].shape:
        raise ValueError("clean_prompt and corrupt_prompt must have the same tokenized shape for this simple patching script.")
    layers = get_decoder_layers(model)
    clean_hidden = {}

    handles = []
    for i, layer in enumerate(layers):
        def save_hook(module, inputs, output, i=i):
            clean_hidden[i] = hidden_from_output(output).detach()
            return output
        handles.append(layer.register_forward_hook(save_hook))
    with torch.no_grad():
        out_clean = model(**clean_inputs, use_cache=False, return_dict=True)
    for h in handles:
        h.remove()

    with torch.no_grad():
        out_corrupt = model(**corrupt_inputs, use_cache=False, return_dict=True)
    clean_score = target_logit(out_clean.logits, target_id)
    corrupt_score = target_logit(out_corrupt.logits, target_id)

    rows = []
    for layer_idx, layer in enumerate(layers):
        def patch_hook(module, inputs, output, layer_idx=layer_idx):
            hidden = hidden_from_output(output).clone()
            hidden[:, args.patch_position, :] = clean_hidden[layer_idx][:, args.patch_position, :]
            return replace_hidden_in_output(output, hidden)
        handle = layer.register_forward_hook(patch_hook)
        with torch.no_grad():
            out_patch = model(**corrupt_inputs, use_cache=False, return_dict=True)
        handle.remove()
        patch_score = target_logit(out_patch.logits, target_id)
        rows.append({
            "model_id": cfg["model_id"], "clean_prompt": clean_prompt, "corrupt_prompt": corrupt_prompt, "target_text": target_text,
            "layer": layer_idx, "intervention": "activation_patch", "patch_position": args.patch_position,
            "clean_target_logit": clean_score, "corrupt_target_logit": corrupt_score, "patched_target_logit": patch_score,
            "recovery_from_corrupt": patch_score - corrupt_score,
            "fraction_of_clean_effect": (patch_score - corrupt_score) / (clean_score - corrupt_score + 1e-8),
        })
        print(rows[-1])
    paths = output_paths(cfg); paths["results"].mkdir(parents=True, exist_ok=True)
    out_path = paths["results"] / f"{file_prefix(cfg)}_activation_patching.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("saved:", out_path)

if __name__ == "__main__":
    main()
