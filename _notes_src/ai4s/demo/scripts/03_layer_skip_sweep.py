import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch

from src.config_utils import file_prefix, load_config, output_paths
from src.model_utils import load_causal_lm
from src.hook_utils import get_decoder_layers, make_skip_block_hook
from src.metrics import next_token_kl, target_logit_drop, top1_token
from src.experiment_utils import require_single_token


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--prompt", default=None)
    p.add_argument("--target-text", default=None)

    # 新增：指定要跳过/测试的层
    # 支持：
    #   all
    #   4
    #   4,5,6
    #   4-8
    #   0,2,5-7
    p.add_argument(
        "--layers",
        default="all",
        help="Layer indices to test or skip. Examples: all, 4, 4,5,6, 4-8, 0,2,5-7",
    )

    # 新增：是否同时跳过多个层
    # 不加这个参数：对指定层逐层 sweep
    # 加这个参数：一次 forward 同时跳过 --layers 中指定的所有层
    p.add_argument(
        "--skip-together",
        action="store_true",
        help="If set, skip all selected layers in one forward pass. Otherwise sweep selected layers one by one.",
    )

    return p.parse_args()


def parse_layer_spec(layer_spec, num_layers):
    """
    Parse layer specification string.

    Examples
    --------
    "all"       -> [0, 1, ..., num_layers-1]
    "4"         -> [4]
    "4,5,6"     -> [4, 5, 6]
    "4-8"       -> [4, 5, 6, 7, 8]
    "0,2,5-7"   -> [0, 2, 5, 6, 7]
    """
    if layer_spec is None or layer_spec == "all":
        return list(range(num_layers))

    selected = []

    for part in layer_spec.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start = int(start_str)
            end = int(end_str)

            if start > end:
                raise ValueError(f"Invalid layer range: {part}")

            selected.extend(list(range(start, end + 1)))
        else:
            selected.append(int(part))

    selected = sorted(set(selected))

    for idx in selected:
        if idx < 0 or idx >= num_layers:
            raise ValueError(
                f"Layer index {idx} out of range. "
                f"Valid layer indices: 0 to {num_layers - 1}"
            )

    return selected


def run_base_forward(model, inputs):
    with torch.no_grad():
        return model(
            **inputs,
            use_cache=False,
            return_dict=True,
        )


def run_single_layer_skip(
    model,
    tokenizer,
    inputs,
    layer,
    layer_idx,
    out_base,
    cfg,
    prompt,
    target_text,
    target_id,
):
    """
    Skip one selected layer and return one result row.
    """
    handle = layer.register_forward_hook(make_skip_block_hook())

    with torch.no_grad():
        out_skip = model(
            **inputs,
            use_cache=False,
            return_dict=True,
        )

    handle.remove()

    top1_base = top1_token(tokenizer, out_base.logits)
    top1_intervened = top1_token(tokenizer, out_skip.logits)

    kl_value = next_token_kl(out_base.logits, out_skip.logits)
    if hasattr(kl_value, "item"):
        kl_value = kl_value.item()

    row = {
        "model_id": cfg["model_id"],
        "prompt": prompt,
        "target_text": target_text,
        "layer": layer_idx,
        "skipped_layers": str([layer_idx]),
        "intervention": "skip_block_single",
        "kl_base_to_intervened": kl_value,
        "target_logit_drop": target_logit_drop(
            out_base.logits,
            out_skip.logits,
            target_id,
        ),
        "top1_base": top1_base,
        "top1_intervened": top1_intervened,
        "top1_change": top1_base != top1_intervened,
    }

    return row


def run_multi_layer_skip(
    model,
    tokenizer,
    inputs,
    layers,
    selected_layers,
    out_base,
    cfg,
    prompt,
    target_text,
    target_id,
):
    """
    Skip all selected layers simultaneously and return one result row.
    """
    handles = []

    for layer_idx in selected_layers:
        handle = layers[layer_idx].register_forward_hook(make_skip_block_hook())
        handles.append(handle)

    with torch.no_grad():
        out_skip = model(
            **inputs,
            use_cache=False,
            return_dict=True,
        )

    for handle in handles:
        handle.remove()

    top1_base = top1_token(tokenizer, out_base.logits)
    top1_intervened = top1_token(tokenizer, out_skip.logits)

    kl_value = next_token_kl(out_base.logits, out_skip.logits)
    if hasattr(kl_value, "item"):
        kl_value = kl_value.item()

    row = {
        "model_id": cfg["model_id"],
        "prompt": prompt,
        "target_text": target_text,
        "layer": "multi",
        "skipped_layers": str(selected_layers),
        "intervention": "skip_block_multi",
        "kl_base_to_intervened": kl_value,
        "target_logit_drop": target_logit_drop(
            out_base.logits,
            out_skip.logits,
            target_id,
        ),
        "top1_base": top1_base,
        "top1_intervened": top1_intervened,
        "top1_change": top1_base != top1_intervened,
    }

    return row


def main():
    args = parse_args()

    cfg = load_config(args.config)
    model, tokenizer, device, _ = load_causal_lm(cfg, args.cache_dir)

    prompt = args.prompt or cfg.get("prompt")
    target_text = args.target_text or cfg.get("target_text")

    if prompt is None:
        raise ValueError("Prompt is missing. Provide --prompt or set 'prompt' in config.")

    if target_text is None:
        raise ValueError("Target text is missing. Provide --target-text or set 'target_text' in config.")

    target_id = require_single_token(tokenizer, target_text)

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    layers = get_decoder_layers(model)
    num_layers = len(layers)

    selected_layers = parse_layer_spec(args.layers, num_layers)

    print(f"Model: {cfg['model_id']}")
    print(f"Number of layers: {num_layers}")
    print(f"Selected layers: {selected_layers}")
    print(f"Skip together: {args.skip_together}")

    out_base = run_base_forward(model, inputs)

    rows = []

    if args.skip_together:
        row = run_multi_layer_skip(
            model=model,
            tokenizer=tokenizer,
            inputs=inputs,
            layers=layers,
            selected_layers=selected_layers,
            out_base=out_base,
            cfg=cfg,
            prompt=prompt,
            target_text=target_text,
            target_id=target_id,
        )
        rows.append(row)
        print(row)

    else:
        for layer_idx in selected_layers:
            row = run_single_layer_skip(
                model=model,
                tokenizer=tokenizer,
                inputs=inputs,
                layer=layers[layer_idx],
                layer_idx=layer_idx,
                out_base=out_base,
                cfg=cfg,
                prompt=prompt,
                target_text=target_text,
                target_id=target_id,
            )
            rows.append(row)
            print(row)

    paths = output_paths(cfg)
    paths["results"].mkdir(parents=True, exist_ok=True)

    layer_tag = args.layers.replace(",", "_").replace("-", "to")

    if args.skip_together:
        out_name = f"{file_prefix(cfg)}_skip_layers_{layer_tag}_together.csv"
    else:
        out_name = f"{file_prefix(cfg)}_layer_skip_sweep_{layer_tag}.csv"

    out_path = paths["results"] / out_name

    pd.DataFrame(rows).to_csv(out_path, index=False)

    print("saved:", out_path)


if __name__ == "__main__":
    main()