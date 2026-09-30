# src/rerun_exp2_from_prev_exp1.py

import os
import argparse
import random
from typing import List

import pandas as pd
import yaml  # 新增：用来读 config.yaml

from api_client import DMXClient
from experiment import ExperimentRunner
from utils import timestamped_outdir, save_jsonl, save_csv_dicts


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Reuse previous Exp1 results and run a new non-uniform Exp2."
    )
    ap.add_argument(
        "--prev_outdir",
        type=str,
        required=True,
        help="Path to previous run output directory (containing sampled_words.csv and exp1_isolated_summary.csv)",
    )

    # 可以通过命令行覆盖，也可以留空走 config.yaml
    ap.add_argument("--base_url", type=str, help="DMXAPI base url")
    ap.add_argument("--api_key", type=str, help="DMXAPI key (prefer config.yaml)")
    ap.add_argument("--model", type=str, help="Model name, e.g. gpt-4o-mini")
    ap.add_argument("--temperature", type=float, help="Sampling temperature")

    ap.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for shuffling / subsampling words for Exp2. "
             "If not set, will use seed from config.yaml or 42 as fallback.",
    )
    ap.add_argument(
        "--n_words_exp2",
        type=int,
        default=None,
        help=(
            "How many words to use in the new Exp2. "
            "If not set, use ALL words from previous sampled_words.csv."
        ),
    )
    ap.add_argument(
        "--dimension",
        type=str,
        default=None,
        choices=["concreteness", "valence", "arousal"],
        help="Rating dimension (should match the previous Exp1 run). "
             "If not set, will use 'rating_dimension' from config.yaml or default to 'concreteness'.",
    )
    ap.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to config.yaml (optional, default: config.yaml in project root)",
    )
    return ap.parse_args()


def load_config(path: str) -> dict:
    """简单版本的 config 加载器。"""
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if not isinstance(cfg, dict):
        raise RuntimeError("config.yaml 必须是一个 YAML 映射（dict）。")
    return cfg


def main() -> None:
    args = parse_args()

    # 1) 先读 config.yaml
    cfg = load_config(args.config)

    prev_dir = args.prev_outdir
    if not os.path.isdir(prev_dir):
        raise FileNotFoundError(f"Previous outdir not found: {prev_dir}")

    # 2) 读入上一次 run 的 sampled_words & exp1 summary
    sampled_path = os.path.join(prev_dir, "sampled_words.csv")
    exp1_sum_path = os.path.join(prev_dir, "exp1_isolated_summary.csv")

    if not os.path.exists(sampled_path):
        raise FileNotFoundError(f"sampled_words.csv not found in: {prev_dir}")
    if not os.path.exists(exp1_sum_path):
        raise FileNotFoundError(f"exp1_isolated_summary.csv not found in: {prev_dir}")

    sampled_prev = pd.read_csv(sampled_path)
    exp1_sum = pd.read_csv(exp1_sum_path)

    if "word" not in sampled_prev.columns:
        raise RuntimeError("sampled_words.csv must contain a 'word' column.")
    if "word" not in exp1_sum.columns:
        raise RuntimeError("exp1_isolated_summary.csv must contain a 'word' column.")

    # 3) 组合配置：命令行 > config.yaml > 默认值
    base_url = args.base_url or cfg.get("base_url", "https://www.dmxapi.cn/v1")

    api_key = args.api_key or cfg.get("api_key")
    if not api_key:
        raise RuntimeError("api_key 没有通过命令行或 config.yaml 提供，请至少用一种方式提供。")

    model = args.model or cfg.get("model", "gpt-4o-mini")
    temperature = (
        args.temperature
        if args.temperature is not None
        else float(cfg.get("temperature", 0.0))
    )

    if args.seed is not None:
        seed = int(args.seed)
    else:
        seed = int(cfg.get("seed", 42))

    if args.dimension is not None:
        dimension = args.dimension
    else:
        dimension = cfg.get("rating_dimension", "concreteness")

    # 所有上次 Exp1 用过的词
    all_words: List[str] = sampled_prev["word"].astype(str).tolist()
    if len(all_words) == 0:
        raise RuntimeError("No words found in previous sampled_words.csv")

    # 4) 决定这次 Exp2 用哪些词（非均匀分布：只是随机打乱 / 抽子集）
    rng = random.Random(seed)
    rng.shuffle(all_words)

    if args.n_words_exp2 is not None:
        n = int(args.n_words_exp2)
        if n <= 0:
            raise ValueError("n_words_exp2 must be > 0")
        if n > len(all_words):
            n = len(all_words)
        exp2_words = all_words[:n]
    else:
        # 默认：用上次 Exp1 的全部词
        exp2_words = all_words

    print(f"Reusing previous Exp1 from: {prev_dir}")
    print(f"Total words in previous Exp1: {len(all_words)}")
    print(f"New Exp2 will use {len(exp2_words)} words.")
    print(f"Model: {model}, temperature: {temperature}, dimension: {dimension}")
    print(f"Using base_url: {base_url}")

    # 5) 创建新的输出目录
    outdir = timestamped_outdir("outputs")
    os.makedirs(outdir, exist_ok=True)
    print(f"New outputs will be written to: {outdir}")

    # 保存这次实际用于 Exp2 的 sampled_words（顺序 = Exp2 询问顺序）
    sampled_subset = sampled_prev[sampled_prev["word"].astype(str).isin(exp2_words)].copy()
    order_map = {w: i for i, w in enumerate(exp2_words)}
    sampled_subset["__order"] = sampled_subset["word"].astype(str).map(order_map)
    sampled_subset = sampled_subset.sort_values("__order").drop(columns=["__order"])
    sampled_subset.to_csv(os.path.join(outdir, "sampled_words.csv"), index=False)

    # 6) 初始化 API 客户端和 Runner（只跑 Exp2）
    client = DMXClient(base_url=base_url, api_key=api_key)
    runner = ExperimentRunner(
        client=client,
        model=model,
        temperature=temperature,
        logs_dir=os.path.join(os.getcwd(), "logs"),
        ci95_enable=False,          # Exp2 不用 CI
        ci95_threshold=0.1,
        max_trials_per_word=1,
        rating_dimension=dimension,
    )

    # 7) 运行新的 Exp2（顺序 = exp2_words）
    exp2_result = runner.run_experiment2_sequential(exp2_words)
    save_jsonl(os.path.join(outdir, "exp2_sequential_raw.jsonl"), exp2_result["raw"])
    save_csv_dicts(os.path.join(outdir, "exp2_sequential_raw.csv"), exp2_result["raw"])

    # 8) 基于“旧 Exp1 + 新 Exp2”构造新的 combined_overview.csv
    exp2_df = pd.DataFrame(exp2_result["raw"]).rename(columns={"rating": "exp2_rating"})
    exp2_df["word"] = exp2_df["word"].astype(str)

    if "chatgpt_concreteness_estimate" in sampled_prev.columns:
        sampled_small = sampled_subset[
            ["word", "chatgpt_concreteness_estimate"]
        ].rename(columns={"chatgpt_concreteness_estimate": "baseline_excel_col6"})
    else:
        sampled_small = sampled_subset[["word"]].copy()
        sampled_small["baseline_excel_col6"] = None

    merged = sampled_small.copy()

    exp1_sum["word"] = exp1_sum["word"].astype(str)
    merged["word"] = merged["word"].astype(str)
    merged = merged.merge(exp1_sum, on="word", how="left", suffixes=("", "_exp1"))

    merged = merged.merge(exp2_df[["word", "exp2_rating"]], on="word", how="left")

    merged.to_csv(os.path.join(outdir, "combined_overview.csv"), index=False)

    print("Done. New Exp2 + combined_overview.csv written to:", outdir)


if __name__ == "__main__":
    main()
