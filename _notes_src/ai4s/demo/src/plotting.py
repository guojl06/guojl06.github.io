from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_layer_metric(csv_path: str | Path, metric: str, out_path: str | Path, title: str | None = None):
    df = pd.read_csv(csv_path)
    if "layer" not in df.columns or metric not in df.columns:
        raise ValueError(f"CSV must contain columns 'layer' and {metric!r}")
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(111)
    ax.plot(df["layer"], df[metric], marker="o")
    ax.set_xlabel("Layer")
    ax.set_ylabel(metric)
    ax.set_title(title or metric)
    fig.tight_layout()
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
