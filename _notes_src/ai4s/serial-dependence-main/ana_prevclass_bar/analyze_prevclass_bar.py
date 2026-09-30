"""Prev-class conditional-mean analysis (Exp2 ratings).

Goal
----
Split the *previous* trial's Exp2 rating into two classes:
  - low:  1–50
  - high: 51–100

Then compute, for all valid lag-1 pairs (t-1 -> t):
  - mean(exp2_rating[t] | exp2_rating[t-1] in low)
  - mean(exp2_rating[t] | exp2_rating[t-1] in high)

Outputs
-------
Saves under:
  <project_root>/ana_prevclass_bar/results/<run_tag>/
    - prevclass_bar.png
    - prevclass_summary.json
    - (optional) prevclass_pairs.csv

Usage
-----
  python analyze_prevclass_bar.py
  python analyze_prevclass_bar.py --outputs-dir outputs
  python analyze_prevclass_bar.py --run-dir outputs/<your_run_tag>
  python analyze_prevclass_bar.py --run-dir outputs/<your_run_tag> --save-pairs-csv
  python analyze_prevclass_bar.py --n-perm 10000
"""
from __future__ import annotations

import os
import sys
import json
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ci_utils import ci95_half_width


plt.rcParams["font.family"] = "DejaVu Sans"


def project_root_dir() -> str:
    """Best-effort project root detection."""
    here = Path(__file__).resolve().parent
    parent = here.parent

    # Most common: this file lives under ana_prevclass_bar/
    if (parent / "config.yaml").exists() or (parent / "outputs").is_dir():
        return str(parent)

    # Flat repo fallback
    if (here / "config.yaml").exists() or (here / "outputs").is_dir():
        return str(here)

    return str(parent)


def find_latest_run(outputs_dir: str) -> str:
    if not os.path.isdir(outputs_dir):
        raise FileNotFoundError(f"Directory not found: {outputs_dir}")
    subdirs = [
        os.path.join(outputs_dir, d)
        for d in os.listdir(outputs_dir)
        if os.path.isdir(os.path.join(outputs_dir, d))
    ]
    if not subdirs:
        raise FileNotFoundError(f"No run subdirectories under: {outputs_dir}")
    return max(subdirs, key=lambda p: os.path.getmtime(p))


def load_dimension(run_dir: str, default: str = "concreteness") -> str:
    cfg_path = os.path.join(run_dir, "run_config.yaml")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            if isinstance(cfg, dict):
                dim = cfg.get("dimension", default)
                if isinstance(dim, str):
                    return dim
        except Exception:
            pass
    return default


def load_exp2_sequence(run_dir: str) -> pd.DataFrame:
    """Load Exp2 sequential ratings in their true temporal order.

    Preference order:
      1) exp2_sequential_raw.csv (has the sequential order by construction)
      2) combined_overview.csv (assumed already ordered by exp2 order)
    """
    p1 = os.path.join(run_dir, "exp2_sequential_raw.csv")
    if os.path.exists(p1):
        df = pd.read_csv(p1)
        # columns: word, rating, text, asked_dimension
        df["exp2_rating"] = pd.to_numeric(df.get("rating"), errors="coerce")
        df["word"] = df.get("word").astype(str)
        out = df[["word", "exp2_rating"]].copy()
        return out

    p2 = os.path.join(run_dir, "combined_overview.csv")
    if not os.path.exists(p2):
        raise FileNotFoundError(
            f"Missing Exp2 outputs. Not found: {p1} nor {p2}. Did you run which=exp2/both?"
        )
    df = pd.read_csv(p2)
    df["exp2_rating"] = pd.to_numeric(df.get("exp2_rating"), errors="coerce")
    df["word"] = df.get("word").astype(str)
    return df[["word", "exp2_rating"]].copy()


def build_prevclass_pairs(df_seq: pd.DataFrame, low_max: int = 50) -> pd.DataFrame:
    df = df_seq.copy()
    df["prev_rating"] = df["exp2_rating"].shift(1)
    df["curr_rating"] = df["exp2_rating"]

    pairs = df.dropna(subset=["prev_rating", "curr_rating"]).copy()
    pairs["prev_rating"] = pairs["prev_rating"].astype(int)
    pairs["curr_rating"] = pairs["curr_rating"].astype(int)

    def _cls(x: int) -> str:
        return "low" if x <= low_max else "high"

    pairs["prev_class"] = pairs["prev_rating"].apply(_cls)
    return pairs[["prev_rating", "prev_class", "curr_rating"]].reset_index(drop=True)


def permutation_pvalue(delta_obs: float, y: np.ndarray, labels: np.ndarray, n_perm: int, seed: int = 0) -> float:
    """Two-sided permutation test by shuffling labels."""
    rng = np.random.default_rng(seed)
    labels = labels.copy()
    n = len(y)
    if n_perm <= 0:
        return float("nan")

    # Encode labels: 0=low, 1=high
    lab01 = (labels == "high").astype(int)
    # precompute indices for speed each perm via permuted lab01
    count = 0
    for _ in range(n_perm):
        rng.shuffle(lab01)
        y_low = y[lab01 == 0]
        y_high = y[lab01 == 1]
        if len(y_low) == 0 or len(y_high) == 0:
            continue
        d = float(np.mean(y_high) - np.mean(y_low))
        if abs(d) >= abs(delta_obs):
            count += 1

    # add-one smoothing
    return (count + 1.0) / (n_perm + 1.0)


def plot_bar(means: dict, errs: dict, save_path: str, title: str) -> None:
    labels = ["prev_low (1–50)", "prev_high (51–100)"]
    y = [means["low"], means["high"]]
    yerr = [errs["low"], errs["high"]]

    x = np.arange(len(labels))
    plt.figure(figsize=(6.0, 4.6), dpi=150)
    plt.bar(x, y, yerr=yerr, capsize=6, alpha=0.9)
    plt.xticks(x, labels, rotation=0)
    plt.ylabel("Mean current Exp2 rating")
    plt.title(title)
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Prev-class conditional mean analysis on Exp2 ratings.")
    ap.add_argument("--outputs-dir", type=str, default="outputs")
    ap.add_argument("--run-dir", type=str, default=None)
    ap.add_argument("--low-max", type=int, default=50, help="low class upper bound (inclusive). Default=50.")
    ap.add_argument(
        "--errorbar",
        type=str,
        default="ci95",
        choices=["ci95", "sem"],
        help="Error bar type: ci95 (default) or sem.",
    )
    ap.add_argument("--save-pairs-csv", action="store_true")
    ap.add_argument("--n-perm", type=int, default=0, help="If >0, run a permutation test with this many shuffles.")
    ap.add_argument("--perm-seed", type=int, default=0)
    args = ap.parse_args()

    run_dir = args.run_dir or find_latest_run(args.outputs_dir)
    run_tag = os.path.basename(os.path.normpath(run_dir))
    dimension = load_dimension(run_dir)

    root = project_root_dir()
    out_dir = os.path.join(root, "ana_prevclass_bar", "results", run_tag)
    os.makedirs(out_dir, exist_ok=True)

    df_seq = load_exp2_sequence(run_dir)
    pairs = build_prevclass_pairs(df_seq, low_max=int(args.low_max))
    if pairs.empty:
        raise RuntimeError("No valid lag-1 pairs found (need >=2 valid Exp2 ratings).")

    y_low = pairs.loc[pairs["prev_class"] == "low", "curr_rating"].to_numpy(dtype=float)
    y_high = pairs.loc[pairs["prev_class"] == "high", "curr_rating"].to_numpy(dtype=float)
    if len(y_low) == 0 or len(y_high) == 0:
        raise RuntimeError(
            f"One group is empty: n_low={len(y_low)}, n_high={len(y_high)}. "
            "This can happen if almost all previous ratings fall into one class."
        )

    means = {"low": float(np.mean(y_low)), "high": float(np.mean(y_high))}
    stds = {"low": float(np.std(y_low, ddof=1)), "high": float(np.std(y_high, ddof=1))}
    ns = {"low": int(len(y_low)), "high": int(len(y_high))}

    if args.errorbar == "sem":
        errs = {
            "low": float(stds["low"] / np.sqrt(ns["low"])),
            "high": float(stds["high"] / np.sqrt(ns["high"])),
        }
        err_note = "SEM"
    else:
        errs = {
            "low": float(ci95_half_width(list(y_low))),
            "high": float(ci95_half_width(list(y_high))),
        }
        err_note = "Normal-approx 95% CI half-width (1.96*s/sqrt(n))"

    delta = float(means["high"] - means["low"])  # difference in conditional means

    # Welch t-test on current ratings, grouped by prev class
    t_res = ttest_ind(y_high, y_low, equal_var=False, nan_policy="omit")

    # Optional permutation test
    perm_p = None
    if int(args.n_perm) > 0:
        perm_p = float(
            permutation_pvalue(
                delta_obs=delta,
                y=pairs["curr_rating"].to_numpy(dtype=float),
                labels=pairs["prev_class"].to_numpy(dtype=str),
                n_perm=int(args.n_perm),
                seed=int(args.perm_seed),
            )
        )

    # Plot
    fig_path = os.path.join(out_dir, "prevclass_bar.png")
    title = f"Prev-class effect on current Exp2 rating ({dimension})\nΔ=mean(high)-mean(low)={delta:.3f}"
    plot_bar(means, errs, fig_path, title=title)

    # Save summary
    summary = {
        "run_dir": run_dir,
        "dimension": dimension,
        "definition": {"low": f"1-{int(args.low_max)}", "high": f"{int(args.low_max)+1}-100"},
        "groups": {
            "prev_low": {
                "n_pairs": ns["low"],
                "mean_curr": means["low"],
                "std_curr": stds["low"],
                "errorbar": errs["low"],
            },
            "prev_high": {
                "n_pairs": ns["high"],
                "mean_curr": means["high"],
                "std_curr": stds["high"],
                "errorbar": errs["high"],
            },
        },
        "delta_high_minus_low": delta,
        "errorbar_note": err_note,
        "welch_ttest": {
            "t_stat": float(t_res.statistic),
            "p_value": float(t_res.pvalue),
        },
        "permutation_test": (None if perm_p is None else {"n_perm": int(args.n_perm), "p_value": perm_p}),
    }
    summary_path = os.path.join(out_dir, "prevclass_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    if args.save_pairs_csv:
        pairs_path = os.path.join(out_dir, "prevclass_pairs.csv")
        pairs.to_csv(pairs_path, index=False)
    else:
        pairs_path = None

    print(f"[OK] Run dir: {run_dir}")
    print(f"[OK] Output dir: {out_dir}")
    print(f"[OK] Figure: {fig_path}")
    print(f"[OK] Summary JSON: {summary_path}")
    if pairs_path:
        print(f"[OK] Pairs CSV: {pairs_path}")


if __name__ == "__main__":
    main()
