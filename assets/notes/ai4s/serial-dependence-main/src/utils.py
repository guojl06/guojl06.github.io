# utils.py
import os, json, csv, random
from datetime import datetime
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd


def timestamped_outdir(base: str = "outputs", tag: str | None = None) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if tag:
        safe_tag = "".join(c if (c.isalnum() or c in "-_.") else "_" for c in tag)
        dirname = f"{ts}_{safe_tag}"
    else:
        dirname = ts

    outdir = os.path.join(base, dirname)
    os.makedirs(outdir, exist_ok=True)
    return outdir


def save_jsonl(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def append_jsonl(path: str, row: Dict[str, Any]):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()


def append_csv_dict(path: str, row: Dict[str, Any], fieldnames: List[str]):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    is_new = (not os.path.exists(path)) or (os.path.getsize(path) == 0)
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        writer.writerow({k: row.get(k, None) for k in fieldnames})
        f.flush()


def save_csv_dicts(path: str, rows: List[Dict[str, Any]]):
    if not rows:
        pd.DataFrame().to_csv(path, index=False)
        return
    keys = sorted({k for r in rows for k in r.keys()})
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def choose_words(clean_df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    rng = random.Random(seed)
    idxs = list(range(len(clean_df)))
    rng.shuffle(idxs)
    take = idxs[:n]
    sampled = clean_df.iloc[take].reset_index(drop=True)
    return sampled


def choose_words_stratified_by_col(
    df: pd.DataFrame,
    n: int,
    seed: int,
    value_col: str,
    n_bins: int = 20,
    value_min: float = 1.0,
    value_max: float = 100.0,
) -> pd.DataFrame:
    """
    "尽量均匀"抽样：按 value_col 在 [value_min,value_max] 等宽分箱，
    每箱尽量取相同数量，不足则从剩余池补齐。最终再整体 shuffle。
    """
    if value_col not in df.columns:
        raise KeyError(f"value_col not found: {value_col}")

    d = df.copy()
    d[value_col] = pd.to_numeric(d[value_col], errors="coerce")
    d = d.dropna(subset=[value_col]).reset_index(drop=True)
    if len(d) < n:
        raise RuntimeError(f"Need n={n} but only {len(d)} rows have finite {value_col}")

    n_bins = int(max(2, n_bins))
    edges = np.linspace(float(value_min), float(value_max), n_bins + 1)
    # include rightmost edge
    bin_idx = np.digitize(d[value_col].to_numpy(dtype=float), edges, right=False) - 1
    bin_idx = np.clip(bin_idx, 0, n_bins - 1)
    d["_bin"] = bin_idx

    rng = random.Random(seed)

    # shuffle indices per bin
    bin_to_idxs: Dict[int, List[int]] = {b: [] for b in range(n_bins)}
    for i, b in enumerate(bin_idx):
        bin_to_idxs[int(b)].append(i)
    for b in range(n_bins):
        rng.shuffle(bin_to_idxs[b])

    base = n // n_bins
    rem = n - base * n_bins

    chosen: List[int] = []
    leftovers: List[int] = []

    for b in range(n_bins):
        want = base + (1 if b < rem else 0)
        xs = bin_to_idxs[b]
        take = xs[: min(want, len(xs))]
        chosen.extend(take)
        leftovers.extend(xs[len(take) :])

    # if not enough (some bins empty), fill from leftovers
    if len(chosen) < n:
        need = n - len(chosen)
        rng.shuffle(leftovers)
        chosen.extend(leftovers[:need])

    # final shuffle order (random permutation of chosen trials)
    rng.shuffle(chosen)

    out = d.iloc[chosen].drop(columns=["_bin"]).reset_index(drop=True)
    return out
