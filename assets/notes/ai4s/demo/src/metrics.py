from __future__ import annotations

from typing import List, Tuple

import torch
import torch.nn.functional as F


def next_token_kl(logits_base, logits_intervened) -> float:
    logp_base = F.log_softmax(logits_base[:, -1, :], dim=-1)
    logp_int = F.log_softmax(logits_intervened[:, -1, :], dim=-1)
    p_base = logp_base.exp()
    return F.kl_div(logp_int, p_base, reduction="batchmean", log_target=False).item()


def target_logit(logits, target_token_id: int) -> float:
    return logits[0, -1, target_token_id].item()


def target_logit_drop(logits_base, logits_intervened, target_token_id: int) -> float:
    return (logits_base[0, -1, target_token_id] - logits_intervened[0, -1, target_token_id]).item()


def topk_tokens(tokenizer, logits, k: int = 10) -> List[Tuple[str, float, int]]:
    values, ids = torch.topk(logits[0, -1], k=k)
    return [(tokenizer.decode([idx.item()]), val.item(), idx.item()) for val, idx in zip(values, ids)]


def top1_token(tokenizer, logits) -> str:
    return topk_tokens(tokenizer, logits, k=1)[0][0]
