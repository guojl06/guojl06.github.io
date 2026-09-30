# ana_none/analyze_none.py
"""Autoregressive analysis for dimension='none' (number-only control).

Reads outputs/<run_tag>/none_autoregressive.csv produced by main.py when
running with dimension='none'. The analysis uses lag-1 pairs (y_{t-1}, y_t)
from the generated numeric sequence, plots a scatter, fits a linear regression
(y_t = intercept + slope * y[t-1]), and saves a figure + JSON summary to:
  <project_root>/ana_none/results/<run_tag>/
"""
import os
import json
import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

plt.rcParams["font.family"] = "DejaVu Sans"

def project_root_dir() -> str:
    """Best-effort project root detection."""
    here = Path(__file__).resolve().parent
    parent = here.parent

    if (parent / "config.yaml").exists() or (parent / "outputs").is_dir():
        return str(parent)

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


def load_none_sequence(run_dir: str) -> pd.DataFrame:
    path = os.path.join(run_dir, "none_autoregressive.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}. Did you run main.py with dimension='none'?")

    df = pd.read_csv(path)
    if "trial" not in df.columns or "rating" not in df.columns:
        raise ValueError(f"Unexpected columns in {path}: {list(df.columns)}")

    df["trial"] = pd.to_numeric(df["trial"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["trial", "rating"]).copy()
    df = df.sort_values("trial").reset_index(drop=True)

    df["y_prev"] = df["rating"].shift(1)
    df["y_curr"] = df["rating"]
    return df.dropna(subset=["y_prev", "y_curr"]).copy()


def plot_scatter_and_fit(x: np.ndarray, y: np.ndarray, res, save_path: str) -> None:
    xs = np.linspace(np.nanmin(x), np.nanmax(x), 400)
    ys = res.intercept + res.slope * xs

    plt.figure(figsize=(6.4, 4.8), dpi=150)
    plt.scatter(x, y, s=18, alpha=0.75, label="Lag-1 pairs")
    plt.plot(xs, ys, lw=2, label="Linear fit")
    plt.xlabel("Previous output y[t-1]")
    plt.ylabel("Current output y[t]")
    subtitle = (
        f"slope={res.slope:.4f}, intercept={res.intercept:.4f}, "
        f"R²={res.rvalue**2:.4f}, p={res.pvalue:.4g}, n={len(x)}"
    )
    plt.title("dimension='none': AR(1) regression\n" + subtitle)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="AR(1) analysis for dimension='none'.")
    parser.add_argument("--outputs-dir", type=str, default="outputs")
    parser.add_argument("--run-dir", type=str, default=None)
    parser.add_argument("--save-scatter-csv", action="store_true")
    args = parser.parse_args()

    run_dir = args.run_dir or find_latest_run(args.outputs_dir)
    run_tag = os.path.basename(os.path.normpath(run_dir))

    root = project_root_dir()
    save_dir = os.path.join(root, "ana_none", "results", run_tag)
    os.makedirs(save_dir, exist_ok=True)

    df_pairs = load_none_sequence(run_dir)
    x = df_pairs["y_prev"].to_numpy(dtype=float)
    y = df_pairs["y_curr"].to_numpy(dtype=float)

    res = linregress(x, y)
    summary = {
        "slope": float(res.slope),
        "intercept": float(res.intercept),
        "r_value": float(res.rvalue),
        "r_squared": float(res.rvalue ** 2),
        "p_value": float(res.pvalue),
        "stderr": float(res.stderr),
        "intercept_stderr": float(getattr(res, "intercept_stderr", np.nan)),
        "n_pairs": int(len(x)),
    }

    fig_path = os.path.join(save_dir, "none_ar1_scatter.png")
    plot_scatter_and_fit(x, y, res, fig_path)

    summary_path = os.path.join(save_dir, "none_ar1_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    if args.save_scatter_csv:
        scatter_path = os.path.join(save_dir, "none_ar1_scatter.csv")
        df_pairs[["trial", "y_prev", "y_curr"]].to_csv(scatter_path, index=False)

    print(f"[OK] Run dir: {run_dir}")
    print(f"[OK] Saved to: {save_dir}")
    print(f"[OK] Figure:  {fig_path}")
    print(f"[OK] Summary: {summary_path}")
    if args.save_scatter_csv:
        print(f"[OK] Scatter CSV: {scatter_path}")


if __name__ == "__main__":
    main()
