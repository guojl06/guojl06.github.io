import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.plotting import plot_layer_metric


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="outputs/results/pythia_70m_layer_skip_sweep.csv")
    p.add_argument("--metric", default="target_logit_drop")
    p.add_argument("--out", default="outputs/figures/layer_metric.png")
    return p.parse_args()


def main():
    args = parse_args()
    plot_layer_metric(args.csv, args.metric, args.out)
    print("saved:", args.out)

if __name__ == "__main__":
    main()
