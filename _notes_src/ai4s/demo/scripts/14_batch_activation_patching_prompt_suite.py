import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from tqdm import tqdm
from src.config_utils import file_prefix, load_config, output_paths
from src.experiment_utils import require_single_token
from src.hook_utils import get_decoder_layers, hidden_from_output, replace_hidden_in_output
from src.metrics import target_logit
from src.model_utils import load_causal_lm
from src.prompt_utils import prompt_suite_from_config, row_tags_json, row_variables_json, validate_prompt_rows


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--prompt-suite", default="prompts/suites/activation_patching_pairs.jsonl")
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--max-examples", type=int, default=None)
    p.add_argument("--skip-invalid", action="store_true")
    p.add_argument("--out", default=None)
    return p.parse_args()


def main():
    args = parse_args(); cfg=load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    rows_in = prompt_suite_from_config(cfg, args.prompt_suite, args.max_examples)
    errors = validate_prompt_rows(rows_in, tokenizer=tokenizer, max_prompt_tokens=cfg.get("experiments", {}).get("global_defaults", {}).get("max_prompt_tokens"))
    if errors and not args.skip_invalid:
        raise ValueError("Prompt validation failed. Use validation script or pass --skip-invalid.")
    bad_ids = {e.get("prompt_id") for e in errors}
    layers = get_decoder_layers(model); rows_out=[]
    for row in tqdm(rows_in, desc="patch-prompts"):
        if args.skip_invalid and row.get("prompt_id") in bad_ids: continue
        clean_prompt, corrupt_prompt = row.get("clean_prompt"), row.get("corrupt_prompt")
        if not clean_prompt or not corrupt_prompt: continue
        target_id = require_single_token(tokenizer, row["target_text"])
        patch_position = int(row.get("patch_position", -1))
        clean_inputs = tokenizer(clean_prompt, return_tensors="pt").to(device)
        corrupt_inputs = tokenizer(corrupt_prompt, return_tensors="pt").to(device)
        if clean_inputs["input_ids"].shape != corrupt_inputs["input_ids"].shape:
            if args.skip_invalid: continue
            raise ValueError(f"Token length mismatch for {row.get('prompt_id')}")
        clean_hidden={}; handles=[]
        for i, layer in enumerate(layers):
            def save_hook(module, inputs, output, i=i):
                clean_hidden[i] = hidden_from_output(output).detach()
                return output
            handles.append(layer.register_forward_hook(save_hook))
        with torch.no_grad(): out_clean = model(**clean_inputs, use_cache=False, return_dict=True)
        for h in handles: h.remove()
        with torch.no_grad(): out_corrupt = model(**corrupt_inputs, use_cache=False, return_dict=True)
        clean_score = target_logit(out_clean.logits,target_id); corrupt_score=target_logit(out_corrupt.logits,target_id)
        for layer_idx, layer in enumerate(layers):
            def patch_hook(module, inputs, output, layer_idx=layer_idx):
                hidden = hidden_from_output(output).clone()
                hidden[:, patch_position, :] = clean_hidden[layer_idx][:, patch_position, :]
                return replace_hidden_in_output(output, hidden)
            handle = layer.register_forward_hook(patch_hook)
            with torch.no_grad(): out_patch = model(**corrupt_inputs, use_cache=False, return_dict=True)
            handle.remove()
            patch_score = target_logit(out_patch.logits,target_id)
            rows_out.append({"model_id":cfg["model_id"],"prompt_id":row.get("prompt_id"),"task":row.get("task"),"condition":row.get("condition"),"intervention":"activation_patch","layer":layer_idx,"patch_position":patch_position,"target_text":row.get("target_text"),"clean_target_logit":clean_score,"corrupt_target_logit":corrupt_score,"patched_target_logit":patch_score,"recovery_from_corrupt":patch_score-corrupt_score,"fraction_of_clean_effect":(patch_score-corrupt_score)/(clean_score-corrupt_score+1e-8),"variables_json":row_variables_json(row),"tags_json":row_tags_json(row)})
    paths=output_paths(cfg); paths["results"].mkdir(parents=True, exist_ok=True)
    out_path=Path(args.out) if args.out else paths["results"] / f"{file_prefix(cfg)}_batch_activation_patching.csv"
    pd.DataFrame(rows_out).to_csv(out_path,index=False); print("saved:",out_path)

if __name__ == "__main__": main()
