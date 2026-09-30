from __future__ import annotations

from typing import Dict, Any, Optional

import torch

from .model_utils import encode, token_ids


def require_single_token(tokenizer, text: str) -> int:
    ids = token_ids(tokenizer, text)
    if len(ids) != 1:
        raise ValueError(f"Expected a single token for target_text={text!r}, got ids={ids}")
    return ids[0]


def forward_prompt(model, tokenizer, device: str, prompt: str, *, use_cache: bool = False, output_hidden_states: bool = False, output_attentions: bool = False):
    inputs = encode(tokenizer, prompt, device)
    with torch.no_grad():
        out = model(
            **inputs,
            use_cache=use_cache,
            output_hidden_states=output_hidden_states,
            output_attentions=output_attentions,
            return_dict=True,
        )
    return out, inputs


def base_result_metadata(cfg: Dict[str, Any], row: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    meta = {
        "model_id": cfg.get("model_id"),
        "config_name": cfg.get("name"),
    }
    if row:
        meta.update({
            "prompt_id": row.get("prompt_id"),
            "task": row.get("task"),
            "condition": row.get("condition"),
            "target_text": row.get("target_text"),
            "expected_answer": row.get("expected_answer"),
        })
    return meta
