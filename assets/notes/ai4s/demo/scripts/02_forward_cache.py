import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import torch
from src.config_utils import file_prefix, load_config, output_paths
from src.model_utils import load_causal_lm


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--prompt", default=None)
    p.add_argument("--save-attentions", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)
    prompt = args.prompt or cfg.get("prompt", "The capital of France is")
    exp = cfg.get("experiments", {}).get("forward_cache", {})
    output_attentions = bool(args.save_attentions or exp.get("output_attentions", False))
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(
            **inputs,
            use_cache=False,
            output_hidden_states=True,
            output_attentions=output_attentions,
            return_dict=True,
        )
    print("logits:", tuple(out.logits.shape))
    print("hidden states:", len(out.hidden_states))
    if out.attentions is not None:
        print("attentions:", len(out.attentions))

    paths = output_paths(cfg)
    paths["activations"].mkdir(parents=True, exist_ok=True)
    save_path = paths["activations"] / f"{file_prefix(cfg)}_forward_cache.pt"
    torch.save({
        "model_id": cfg["model_id"],
        "prompt": prompt,
        "input_ids": inputs["input_ids"].detach().cpu(),
        "logits": out.logits.detach().cpu(),
        "hidden_states": [h.detach().cpu() for h in out.hidden_states],
        "attentions": None if out.attentions is None else [a.detach().cpu() for a in out.attentions],
    }, save_path)
    print("saved:", save_path)

if __name__ == "__main__":
    main()
