"""
2D serial-dependence analysis: scatter + binned curve + linear fit (on binned points).

This script is for runs created with:
  python main.py --2D <dim1> <dim2>

In 2D mode, each run produces THREE variants in the same run folder:
  - order12: dim1 then dim2
  - order21: dim2 then dim1
  - rand:    per-word random prompt order

For each (variant, dimension):
  - Response bias: e = exp2_rating_dim - exp1_mean_dim
  - Predictor:     R = exp1_mean_dim[t-1] - exp1_mean_dim[t]
  - Scatter of (R, e)
  - Bin along R, average e per bin -> binned curve
  - Fit OLS on binned points: e_mean ~ R_mid
  - Save ONE figure that overlays scatter, binned curve, and linear fit.

Outputs:
  <project_root>/figures/<run_tag>/2d_bin_linear/<variant>/<dimension>_scatter_binned_linear.png
  <project_root>/figures/<run_tag>/2d_bin_linear/<variant>/<dimension>_summary.json
  <project_root>/figures/<run_tag>/2d_bin_linear/<variant>/<dimension>_binned_curve.csv
"""

from __future__ import annotations

import os
import json
import argparse
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

import yaml

plt.rcParams["font.family"] = "DejaVu Sans"


def project_root_dir() -> str:
    """Best-effort project root detection."""
    here = os.path.abspath(os.path.dirname(__file__))
    parent = os.path.abspath(os.path.join(here, ".."))

    if os.path.exists(os.path.join(here, "config.yaml")) or os.path.isdir(os.path.join(here, "outputs")):
        return here
    if os.path.exists(os.path.join(parent, "config.yaml")) or os.path.isdir(os.path.join(parent, "outputs")):
        return parent
    return here


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


def load_run_config(run_dir: str) -> Dict[str, Any]:
    cfg_path = os.path.join(run_dir, "run_config.yaml")
    if not os.path.exists(cfg_path):
        return {}
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        if isinstance(cfg, dict):
            return cfg
    except Exception:
        pass
    return {}


def bin_curve(df_clean: pd.DataFrame, n_bins: int) -> pd.DataFrame:
    """Bin along R and average e within each bin."""
    if n_bins <= 0:
        raise ValueError("n_bins must be a positive integer")

    R = df_clean["R"].to_numpy(dtype=float)
    e = df_clean["e"].to_numpy(dtype=float)

    r_min = float(np.nanmin(R))
    r_max = float(np.nanmax(R))
    if not np.isfinite(r_min) or not np.isfinite(r_max):
        raise RuntimeError("R contains no finite values.")
    if r_min == r_max:
        raise RuntimeError("All R values are identical; cannot form bins.")

    bin_edges = np.linspace(r_min, r_max, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    tmp = pd.DataFrame({"R": R, "e": e})
    tmp["bin"] = pd.cut(tmp["R"], bins=bin_edges, include_lowest=True, labels=False)
    tmp = tmp.dropna(subset=["bin"]).copy()
    tmp["bin"] = tmp["bin"].astype(int)

    grouped = (
        tmp.groupby("bin")
        .agg(
            e_mean=("e", "mean"),
            count=("e", "size"),
        )
        .reset_index()
    )
    grouped["R_mid"] = grouped["bin"].apply(lambda i: float(bin_centers[i]))

    grouped = grouped[["bin", "R_mid", "e_mean", "count"]].sort_values("R_mid").reset_index(drop=True)
    return grouped


def prepare_e_R(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    """Compute e and R for a given dimension."""
    mean_col = f"mean_{dim}"
    exp2_col = f"exp2_rating_{dim}"

    out = df.copy()
    out["exp1_mean"] = pd.to_numeric(out.get(mean_col), errors="coerce")
    out["exp2_rating"] = pd.to_numeric(out.get(exp2_col), errors="coerce")

    out["e"] = out["exp2_rating"] - out["exp1_mean"]
    out["R"] = out["exp1_mean"].shift(1) - out["exp1_mean"]

    clean = out.dropna(subset=["e", "R"]).copy()
    return clean


def plot_one(
    df_clean: pd.DataFrame,
    binned_df: pd.DataFrame,
    lin_res,
    save_path: str,
    run_tag: str,
    variant: str,
    dim: str,
) -> None:
    """One figure: scatter + binned curve + linear fit."""
    R = df_clean["R"].to_numpy(dtype=float)
    e = df_clean["e"].to_numpy(dtype=float)

    x = binned_df["R_mid"].to_numpy(dtype=float)
    y = binned_df["e_mean"].to_numpy(dtype=float)

    xs = np.linspace(float(np.nanmin(x)), float(np.nanmax(x)), 400)
    ys = lin_res.intercept + lin_res.slope * xs

    subtitle = (
        f"OLS on binned points: slope={lin_res.slope:.4f}, intercept={lin_res.intercept:.4f}, "
        f"R²={lin_res.rvalue**2:.4f}, p={lin_res.pvalue:.4g}, "
        f"n_raw={len(df_clean)}, n_bins={len(binned_df)}"
    )

    plt.figure(figsize=(6.4, 4.8), dpi=150)
    plt.scatter(R, e, s=12, alpha=0.30, label="Raw scatter")
    plt.plot(x, y, marker="o", linestyle="-", linewidth=2, markersize=4, alpha=0.90, label="Binned mean")
    plt.plot(xs, ys, linewidth=2, label="Linear fit (binned)")
    plt.axhline(0, lw=1, ls="--")
    plt.axvline(0, lw=1, ls="--")
    plt.xlabel("R = exp1_mean[t-1] - exp1_mean[t]")
    plt.ylabel("e = exp2_rating - exp1_mean")
    plt.title(f"2D Serial dependence | {run_tag}\n{variant} | {dim}\n{subtitle}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="2D serial-dependence analysis: scatter + binned + linear fit")
    parser.add_argument("--outputs-dir", type=str, default="outputs")
    parser.add_argument(
        "--run-dir",
        type=str,
        default=None,
        help="Specific run folder (e.g., outputs/2025-11-08_15-02-31_...). If not set, use latest.",
    )
    parser.add_argument("--n-bins", type=int, default=20, help="Number of bins along R (default: 20).")
    args = parser.parse_args()

    run_dir = args.run_dir or find_latest_run(args.outputs_dir)
    run_tag = os.path.basename(os.path.normpath(run_dir))

    cfg = load_run_config(run_dir)
    if str(cfg.get("dimension", "")).lower() != "2d":
        print(f"[WARN] run_config.yaml dimension is not '2d' (got: {cfg.get('dimension')}). Will still try to run.")

    dims = cfg.get("two_d_dimensions")
    if not isinstance(dims, (list, tuple)) or len(dims) != 2:
        raise RuntimeError("Missing two_d_dimensions in run_config.yaml (expected list of length 2).")

    dim1, dim2 = str(dims[0]), str(dims[1])
    variants: List[str] = cfg.get("two_d_variants") or ["order12", "order21", "rand"]

    root = project_root_dir()
    out_root = os.path.join(root, "figures", run_tag, "2d_bin_linear")
    os.makedirs(out_root, exist_ok=True)

    all_summaries: Dict[str, Any] = {
        "run_dir": run_dir,
        "run_tag": run_tag,
        "two_d_dimensions": [dim1, dim2],
        "n_bins": int(args.n_bins),
        "variants": {},
    }

    for variant in variants:
        overview_path = os.path.join(run_dir, f"combined_overview_{variant}.csv")
        if not os.path.exists(overview_path):
            print(f"[SKIP] Missing combined_overview for variant '{variant}': {overview_path}")
            continue

        df = pd.read_csv(overview_path)

        var_out = os.path.join(out_root, variant)
        os.makedirs(var_out, exist_ok=True)

        all_summaries["variants"][variant] = {}

        for dim in (dim1, dim2):
            df_clean = prepare_e_R(df, dim)
            if df_clean.empty:
                print(f"[SKIP] No valid (R,e) for variant={variant}, dim={dim}.")
                continue

            binned_df = bin_curve(df_clean, args.n_bins)
            if len(binned_df) < 2:
                print(f"[SKIP] Not enough non-empty bins for variant={variant}, dim={dim}. Try smaller --n-bins")
                continue

            res = linregress(binned_df["R_mid"].to_numpy(dtype=float), binned_df["e_mean"].to_numpy(dtype=float))

            fig_path = os.path.join(var_out, f"{dim}_scatter_binned_linear.png")
            plot_one(df_clean, binned_df, res, fig_path, run_tag=run_tag, variant=variant, dim=dim)

            binned_path = os.path.join(var_out, f"{dim}_binned_curve.csv")
            binned_df.to_csv(binned_path, index=False)

            summary = {
                "variant": variant,
                "dimension": dim,
                "run_dir": run_dir,
                "run_tag": run_tag,
                "predictor": "R = exp1_mean[t-1] - exp1_mean[t]",
                "response": "e = exp2_rating - exp1_mean",
                "n_points_raw": int(len(df_clean)),
                "n_bins_requested": int(args.n_bins),
                "n_bins_used": int(len(binned_df)),
                "ols_on_binned": {
                    "slope": float(res.slope),
                    "intercept": float(res.intercept),
                    "r_value": float(res.rvalue),
                    "r_squared": float(res.rvalue ** 2),
                    "p_value": float(res.pvalue),
                    "stderr": float(res.stderr),
                    "intercept_stderr": float(getattr(res, "intercept_stderr", np.nan)),
                },
                "paths": {
                    "figure": fig_path,
                    "binned_curve_csv": binned_path,
                },
            }

            summary_path = os.path.join(var_out, f"{dim}_summary.json")
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)

            all_summaries["variants"][variant][dim] = summary

            print(f"[OK] {variant} | {dim} -> {fig_path}")

    index_path = os.path.join(out_root, "_2d_bin_linear_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, ensure_ascii=False, indent=2)

    print(f"[OK] Output root: {out_root}")
    print(f"[OK] Index JSON:  {index_path}")


if __name__ == "__main__":
    main()
