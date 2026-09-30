from __future__ import annotations

from typing import Any

import torch


def get_decoder_layers(model):
    if hasattr(model, "model") and hasattr(model.model, "layers"):
        return model.model.layers
    if hasattr(model, "transformer") and hasattr(model.transformer, "h"):
        return model.transformer.h
    if hasattr(model, "gpt_neox") and hasattr(model.gpt_neox, "layers"):
        return model.gpt_neox.layers
    if hasattr(model, "base_model"):
        return get_decoder_layers(model.base_model)
    raise ValueError("Cannot find decoder layers. Inspect model architecture manually.")


def get_attn_module(block):
    for name in ["self_attn", "attn", "attention"]:
        if hasattr(block, name):
            return getattr(block, name)
    raise ValueError(f"Cannot find attention module in block type {type(block)}")


def get_mlp_module(block):
    for name in ["mlp", "feed_forward", "ffn", "dense_h_to_4h"]:
        if hasattr(block, name):
            return getattr(block, name)
    raise ValueError(f"Cannot find MLP module in block type {type(block)}")


def get_final_norm(model):
    if hasattr(model, "model") and hasattr(model.model, "norm"):
        return model.model.norm
    if hasattr(model, "transformer") and hasattr(model.transformer, "ln_f"):
        return model.transformer.ln_f
    if hasattr(model, "gpt_neox") and hasattr(model.gpt_neox, "final_layer_norm"):
        return model.gpt_neox.final_layer_norm
    return None


def make_skip_block_hook():
    def hook(module, inputs, output):
        hidden_in = inputs[0]
        if isinstance(output, tuple):
            return (hidden_in,) + output[1:]
        return hidden_in
    return hook


def make_zero_tensor_hook():
    def hook(module, inputs, output):
        if isinstance(output, tuple):
            x = output[0]
            return (torch.zeros_like(x),) + output[1:]
        return torch.zeros_like(output)
    return hook


def hidden_from_output(output):
    return output[0] if isinstance(output, tuple) else output


def replace_hidden_in_output(output, new_hidden):
    if isinstance(output, tuple):
        return (new_hidden,) + output[1:]
    return new_hidden
