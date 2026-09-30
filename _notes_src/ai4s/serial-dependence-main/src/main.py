# main.py
import os
import sys
import argparse
import yaml
import random
from typing import Dict, Any, List, Optional, Tuple
import time

import pandas as pd

from api_client import DMXClient
from data_loader import load_word_source
from utils import (
    timestamped_outdir,
    save_jsonl,
    save_csv_dicts,
    choose_words,
    choose_words_stratified_by_col,
)
from experiment import ExperimentRunner
from prompts import VALID_EMOTION_TYPES, normalize_emotion_type


VALID_SINGLE_DIMS = ("concreteness", "valence", "arousal", "emotion")
VALID_DIMS = ("concreteness", "valence", "arousal", "emotion", "none", "mixed", "2d")


def load_config(cli_args: argparse.Namespace) -> Dict[str, Any]:
    cfg: Dict[str, Any] = {}

    config_path = cli_args.config or "config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            file_cfg = yaml.safe_load(f) or {}
            if not isinstance(file_cfg, dict):
                raise RuntimeError("config.yaml 必须是一个 YAML 映射（dict）。")
            cfg.update(file_cfg)

    cli_dict = vars(cli_args)
    for k, v in cli_dict.items():
        if k == "config":
            continue
        if v is None:
            continue
        if isinstance(v, bool) and v is False:
            continue
        cfg[k] = v

    return cfg


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, help="Path to config.yaml (optional)")
    ap.add_argument("--base_url", type=str, help="DMXAPI base url")
    ap.add_argument("--api_key", type=str, help="DMXAPI key (prefer config.yaml)")
    ap.add_argument("--model", type=str, help="Model name, e.g. gpt-4o-mini")
    ap.add_argument("--temperature", type=float, help="Sampling temperature")
    ap.add_argument("--which", type=str, choices=["exp1", "exp2", "both"], help="Which experiment(s) to run")
    ap.add_argument("--n_words", type=int, help="Number of words sampled from source for Exp1 (and default Exp2)")
    ap.add_argument("--seed", type=int, default=None, help="Random seed (optional). If omitted, auto-generate.")
    ap.add_argument("--excel_path", type=str, help="Path to word source (.xlsx / Warriner .csv / NRC emotion .txt)")
    ap.add_argument("--dimension", type=str, choices=list(VALID_DIMS), help="Explicit dimension name")
    ap.add_argument("--emotion_type", type=str, default=None, choices=list(VALID_EMOTION_TYPES), help="Target emotion when dimension=emotion (default: joy)")
    ap.add_argument("--ci95_enable", action="store_true", help="Enable adaptive stopping based on 95%% CI half-width")
    ap.add_argument("--ci95_threshold", type=float, help="Target half-width (±) for 95%% CI when ci95_enable is true")
    ap.add_argument("--max_trials_per_word", type=int, help="Max ratings per word for Exp1")
    ap.add_argument("--exp2_context_window", type=int, default=None, help="Keep only last K completed trials as context for Exp2")
    ap.add_argument("--n_words_exp2", type=int, help="Number of words used in Experiment 2 (subset of Exp1 words).")
    ap.add_argument("--n_trials_none", type=int, help="Number of trials for dimension='none'.")

    ap.add_argument("--warriner_max_sd_sum", type=float, default=None, help="Filter: SD.Sum < this (default 1.7)")
    ap.add_argument("--warriner_max_mf_diff", type=float, default=None, help="Filter: |Mean.M-Mean.F| <= this (default 0.5)")
    ap.add_argument("--warriner_n_bins", type=int, default=None, help="Stratified sampling bins (default 20)")

    dim_group = ap.add_mutually_exclusive_group()
    dim_group.add_argument("--concreteness", action="store_true", help="Use concreteness ratings (default).")
    dim_group.add_argument("--valence", action="store_true", help="Use valence ratings.")
    dim_group.add_argument("--arousal", action="store_true", help="Use arousal ratings.")
    dim_group.add_argument("--emotion", action="store_true", help="Use NRC emotion-intensity ratings.")
    dim_group.add_argument("--none", action="store_true", help="Use number-only autoregressive control condition.")
    dim_group.add_argument(
        "--mixed",
        nargs=2,
        metavar=("DIM1", "DIM2"),
        choices=list(VALID_SINGLE_DIMS),
        help="Mixed alternating dimensions. Example: --mixed concreteness arousal",
    )
    dim_group.add_argument(
        "--2D",
        dest="two_d",
        nargs=2,
        metavar=("DIM1", "DIM2"),
        choices=list(VALID_SINGLE_DIMS),
        help="2D ratings in ONE prompt. Example: --2D valence arousal",
    )
    return ap.parse_args()


def _parse_dimension_and_mixed(cfg: Dict[str, Any]) -> Tuple[str, Optional[List[str]], Optional[List[str]]]:
    mixed_dims = None
    two_d_dims = None

    if cfg.get("two_d") is not None:
        two_d_dims = cfg.get("two_d")
        dimension = "2d"
    elif cfg.get("mixed") is not None:
        mixed_dims = cfg.get("mixed")
        dimension = "mixed"
    else:
        dimension = cfg.get("dimension", "concreteness")

        if cfg.get("valence"):
            dimension = "valence"
        elif cfg.get("arousal"):
            dimension = "arousal"
        elif cfg.get("emotion"):
            dimension = "emotion"
        elif cfg.get("concreteness"):
            dimension = "concreteness"
        elif cfg.get("none"):
            dimension = "none"

        if dimension == "mixed":
            mixed_dims = cfg.get("mixed_dimensions") or cfg.get("mixed_dims")
        if dimension == "2d":
            two_d_dims = cfg.get("two_d_dimensions") or cfg.get("two_d_dims")

    if dimension not in VALID_DIMS:
        raise ValueError(f"Invalid dimension: {dimension}")

    if dimension == "mixed":
        if not isinstance(mixed_dims, (list, tuple)) or len(mixed_dims) != 2:
            raise ValueError("dimension='mixed' requires two dims.")
        d1, d2 = str(mixed_dims[0]), str(mixed_dims[1])
        if d1 not in VALID_SINGLE_DIMS or d2 not in VALID_SINGLE_DIMS:
            raise ValueError(f"mixed dims must be in {VALID_SINGLE_DIMS}, got: {mixed_dims}")
        if d1 == d2:
            raise ValueError("mixed dims must be two DIFFERENT dimensions.")
        return "mixed", [d1, d2], None

    if dimension == "2d":
        if not isinstance(two_d_dims, (list, tuple)) or len(two_d_dims) != 2:
            raise ValueError("dimension='2d' requires two dims.")
        d1, d2 = str(two_d_dims[0]), str(two_d_dims[1])
        if d1 not in VALID_SINGLE_DIMS or d2 not in VALID_SINGLE_DIMS:
            raise ValueError(f"2d dims must be in {VALID_SINGLE_DIMS}, got: {two_d_dims}")
        if d1 == d2:
            raise ValueError("2d dims must be two DIFFERENT dimensions.")
        return "2d", None, [d1, d2]

    return str(dimension), None, None


def _alternating_dims_for_length(n: int, dim1: str, dim2: str) -> List[str]:
    return [dim1 if (i % 2 == 0) else dim2 for i in range(n)]


def _reorder_words_to_alternate_dims(
    words: List[str],
    word_to_dim: Dict[str, str],
    dim1: str,
    dim2: str,
    seed: int,
) -> List[str]:
    g1 = [w for w in words if word_to_dim.get(w) == dim1]
    g2 = [w for w in words if word_to_dim.get(w) == dim2]

    rng = random.Random(seed)
    rng.shuffle(g1)
    rng.shuffle(g2)

    out: List[str] = []
    turn = dim1
    while g1 or g2:
        if turn == dim1:
            if g1:
                out.append(g1.pop())
                turn = dim2
            elif g2:
                out.append(g2.pop())
        else:
            if g2:
                out.append(g2.pop())
                turn = dim1
            elif g1:
                out.append(g1.pop())
    return out


def _dims_for_word_source(dimension: str, mixed_dims: Optional[List[str]], two_d_dims: Optional[List[str]]) -> List[str]:
    if dimension in ("valence", "arousal", "concreteness", "emotion"):
        return [dimension]
    if dimension == "mixed":
        assert mixed_dims is not None
        return [str(mixed_dims[0]), str(mixed_dims[1])]
    if dimension == "2d":
        assert two_d_dims is not None
        return [str(two_d_dims[0]), str(two_d_dims[1])]
    return []


def _build_baseline_df(
    sampled: pd.DataFrame,
    dimension: str,
    mixed_dims: Optional[List[str]],
    two_d_dims: Optional[List[str]],
) -> pd.DataFrame:
    base = pd.DataFrame()
    base["word"] = sampled["word"].astype(str)

    if "chatgpt_concreteness_estimate" in sampled.columns:
        base["baseline_excel_col6"] = sampled["chatgpt_concreteness_estimate"]
        return base

    dim = str(dimension).lower()
    if dim in ("valence", "arousal"):
        col = f"{dim}_mean_1_100"
        if col in sampled.columns:
            base["baseline_excel_col6"] = sampled[col]
            return base

    if dim == "emotion" and "emotion_mean_1_100" in sampled.columns:
        base["baseline_excel_col6"] = sampled["emotion_mean_1_100"]
        return base

    base["baseline_excel_col6"] = pd.NA
    return base


def main() -> None:
    args = parse_args()
    cfg = load_config(args)

    base_url = cfg.get("base_url", "https://www.dmxapi.cn/v1")
    api_key = cfg.get("api_key")
    model = cfg.get("model", "gpt-4o-mini")
    temperature = float(cfg.get("temperature", 0.0))
    which = cfg.get("which", "both")
    n_words = int(cfg.get("n_words", 400))

    seed_cfg = cfg.get("seed", None)
    if seed_cfg is None:
        seed = int(time.time_ns() & 0xFFFFFFFF)
        print(f"[INFO] seed not provided; auto seed={seed}", file=sys.stderr)
    else:
        seed = int(seed_cfg)

    excel_path = cfg.get("excel_path", "testing_data/Estimates concreteness words Brysbaert et al.xlsx")
    ci95_enable = bool(cfg.get("ci95_enable", False))
    ci95_threshold = float(cfg.get("ci95_threshold", 0.1))
    max_trials_per_word = int(cfg.get("max_trials_per_word", 20))

    dimension, mixed_dimensions, two_d_dimensions = _parse_dimension_and_mixed(cfg)
    emotion_type = normalize_emotion_type(cfg.get("emotion_type", "joy"))

    n_words_exp2_cfg = cfg.get("n_words_exp2", None)
    n_words_exp2 = int(n_words_exp2_cfg) if n_words_exp2_cfg is not None else None

    n_trials_none_cfg = cfg.get("n_trials_none", None)
    n_trials_none = int(n_trials_none_cfg) if n_trials_none_cfg is not None else 200

    if dimension == "none":
        tag_parts = [model, "none", f"t{n_trials_none}"]
    elif dimension == "mixed":
        d1, d2 = mixed_dimensions[0], mixed_dimensions[1]  # type: ignore[index]
        tag_parts = [model, which, f"mixed_{d1}_{d2}", f"n{n_words}"]
        if n_words_exp2 is not None:
            tag_parts.append(f"exp2_{n_words_exp2}")
    elif dimension == "2d":
        assert two_d_dimensions is not None
        d1, d2 = two_d_dimensions[0], two_d_dimensions[1]
        tag_parts = [model, which, f"2D_{d1}_{d2}", f"n{n_words}"]
        if n_words_exp2 is not None:
            tag_parts.append(f"exp2_{n_words_exp2}")
    elif dimension == "emotion":
        tag_parts = [model, which, f"emotion_{emotion_type}", f"n{n_words}"]
        if n_words_exp2 is not None:
            tag_parts.append(f"exp2_{n_words_exp2}")
    else:
        tag_parts = [model, which, dimension, f"n{n_words}"]
        if n_words_exp2 is not None:
            tag_parts.append(f"exp2_{n_words_exp2}")

    tag = "_".join(tag_parts)

    tmp_outdir = timestamped_outdir("outputs")
    outdir = f"{tmp_outdir}_{tag}"
    try:
        os.rename(tmp_outdir, outdir)
    except Exception:
        outdir = tmp_outdir
    os.makedirs(outdir, exist_ok=True)

    run_config: Dict[str, Any] = {
        "base_url": base_url,
        "model": model,
        "temperature": float(temperature),
        "which": which,
        "dimension": dimension,
        "emotion_type": emotion_type if dimension == "emotion" else None,
        "mixed_dimensions": mixed_dimensions if dimension == "mixed" else None,
        "two_d_dimensions": two_d_dimensions if dimension == "2d" else None,
        "two_d_variants": ["order12", "order21", "rand"] if dimension == "2d" else None,
        "n_words": int(n_words),
        "n_words_exp2": int(n_words_exp2) if n_words_exp2 is not None else None,
        "n_trials_none": int(n_trials_none) if dimension == "none" else None,
        "seed": int(seed),
        "excel_path": excel_path,
        "ci95_enable": bool(ci95_enable),
        "ci95_threshold": float(ci95_threshold),
        "max_trials_per_word": int(max_trials_per_word),
        "merged_cfg": cfg,
        "cli_args": vars(args),
    }

    if dimension == "none":
        if float(temperature) == 0.0:
            print(
                "[WARN] dimension='none' with temperature=0.0 may be near-deterministic; consider temperature > 0.",
                file=sys.stderr,
            )

        client = DMXClient(base_url=base_url, api_key=api_key)
        runner = ExperimentRunner(
            client=client,
            model=model,
            temperature=temperature,
            logs_dir=os.path.join(os.getcwd(), "logs"),
            ci95_enable=ci95_enable,
            ci95_threshold=ci95_threshold,
            max_trials_per_word=max_trials_per_word,
            rating_dimension="none",
            emotion_type=emotion_type,
        )

        with open(os.path.join(outdir, "run_config.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(run_config, f, allow_unicode=True, sort_keys=False)

        none_result = runner.run_none_autoregressive(n_trials_none)
        save_jsonl(os.path.join(outdir, "none_autoregressive_raw.jsonl"), none_result["raw"])
        save_csv_dicts(os.path.join(outdir, "none_autoregressive.csv"), none_result["raw"])
        print(f"Done. Outputs written to: {outdir}")
        return

    dims_for_source = _dims_for_word_source(dimension, mixed_dimensions, two_d_dimensions)

    warriner_max_sd_sum = float(cfg.get("warriner_max_sd_sum", 1.7))
    warriner_max_mf_diff = float(cfg.get("warriner_max_mf_diff", 0.5))
    warriner_n_bins = int(cfg.get("warriner_n_bins", 20))

    clean_df, source_meta = load_word_source(
        excel_path,
        dims_for_warriner=dims_for_source,
        warriner_max_sd_sum=warriner_max_sd_sum,
        warriner_max_mf_diff=warriner_max_mf_diff,
        emotion_type=emotion_type,
    )

    if len(clean_df) < n_words:
        raise RuntimeError(f"想采样 {n_words} 个词，但可用词只有 {len(clean_df)} 个。")

    word_sampling_meta: Dict[str, Any] = {}
    source_type = source_meta.get("source_type")

    if source_type == "warriner_vad":
        if dimension in ("valence", "arousal"):
            value_col = f"{dimension}_mean_1_100"
            if value_col not in clean_df.columns:
                raise RuntimeError(f"Warriner df missing {value_col}")
            sampled = choose_words_stratified_by_col(
                clean_df,
                n=n_words,
                seed=seed,
                value_col=value_col,
                n_bins=warriner_n_bins,
                value_min=1.0,
                value_max=100.0,
            )
            word_sampling_meta = {"method": "stratified_equal_width", "value_col": value_col, "n_bins": warriner_n_bins}
        else:
            cols = []
            for d0 in dims_for_source:
                d0 = str(d0).lower()
                if d0 in ("valence", "arousal"):
                    c = f"{d0}_mean_1_100"
                    if c in clean_df.columns:
                        cols.append(c)
            if not cols:
                raise RuntimeError("Warriner word source requires dims among valence/arousal for mixed/2d.")
            tmp = clean_df.copy()
            tmp["_sampling_value"] = tmp[cols].mean(axis=1)
            sampled = choose_words_stratified_by_col(
                tmp,
                n=n_words,
                seed=seed,
                value_col="_sampling_value",
                n_bins=warriner_n_bins,
                value_min=1.0,
                value_max=100.0,
            ).drop(columns=["_sampling_value"], errors="ignore")
            word_sampling_meta = {"method": "stratified_equal_width", "value_col": f"mean({cols})", "n_bins": warriner_n_bins}

        rng = random.Random(seed)
        idxs = list(range(len(sampled)))
        rng.shuffle(idxs)
        sampled = sampled.iloc[idxs].reset_index(drop=True)
    elif source_type == "nrc_emotion_intensity":
        value_col = "emotion_mean_1_100"
        sampled = choose_words_stratified_by_col(
            clean_df,
            n=n_words,
            seed=seed,
            value_col=value_col,
            n_bins=warriner_n_bins,
            value_min=1.0,
            value_max=100.0,
        )
        word_sampling_meta = {
            "method": "stratified_equal_width",
            "value_col": value_col,
            "n_bins": warriner_n_bins,
            "emotion_type": emotion_type,
        }
        rng = random.Random(seed)
        idxs = list(range(len(sampled)))
        rng.shuffle(idxs)
        sampled = sampled.iloc[idxs].reset_index(drop=True)
    else:
        sampled = choose_words(clean_df, n_words, seed)
        word_sampling_meta = {"method": "random_shuffle"}

    sampled.to_csv(os.path.join(outdir, "sampled_words.csv"), index=False)

    run_config["word_source_meta"] = source_meta
    run_config["word_sampling_meta"] = word_sampling_meta

    with open(os.path.join(outdir, "run_config.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(run_config, f, allow_unicode=True, sort_keys=False)

    words: List[str] = sampled["word"].astype(str).tolist()
    exp2_words: List[str] = list(words)

    word_to_dim: Optional[Dict[str, str]] = None
    exp1_dims: Optional[List[str]] = None
    if dimension == "mixed":
        d1, d2 = mixed_dimensions[0], mixed_dimensions[1]  # type: ignore[index]
        exp1_dims = _alternating_dims_for_length(len(words), d1, d2)
        word_to_dim = {w: exp1_dims[i] for i, w in enumerate(words)}

    client = DMXClient(base_url=base_url, api_key=api_key)
    runner = ExperimentRunner(
        client=client,
        model=model,
        temperature=temperature,
        logs_dir=os.path.join(os.getcwd(), "logs"),
        ci95_enable=ci95_enable,
        ci95_threshold=ci95_threshold,
        max_trials_per_word=max_trials_per_word,
        rating_dimension=(mixed_dimensions[0] if dimension == "mixed" else dimension),  # type: ignore[index]
        emotion_type=emotion_type,
    )

    exp1_result: Dict[str, Any] | None = None
    exp2_result: Dict[str, Any] | None = None

    if which in ("exp1", "both"):
        exp1_result = runner.run_experiment1_isolated(words, dimensions=exp1_dims)
        save_jsonl(os.path.join(outdir, "exp1_isolated_raw.jsonl"), exp1_result["raw"])
        save_csv_dicts(os.path.join(outdir, "exp1_isolated_raw.csv"), exp1_result["raw"])
        save_csv_dicts(os.path.join(outdir, "exp1_isolated_summary.csv"), exp1_result["summary"])

        if which == "both" and n_words_exp2 is not None:
            sum_df = pd.DataFrame(exp1_result["summary"])
            sum_df = sum_df.dropna(subset=["mean"]).copy()
            sum_df["word"] = sum_df["word"].astype(str)
            sum_df = sum_df[sum_df["word"].isin(words)]
            if sum_df.empty:
                raise RuntimeError("Exp1 没有可用的 mean 结果，无法为 Exp2 选词。")

            target_n = int(n_words_exp2)
            if target_n < 1:
                raise ValueError("n_words_exp2 必须 >= 1。")
            if target_n > len(sum_df):
                target_n = len(sum_df)

            sum_df = sum_df.sort_values("mean").reset_index(drop=True)
            N = len(sum_df)
            indices = [k * N // target_n for k in range(target_n)]
            chosen_df = sum_df.iloc[indices].copy()
            chosen_words = chosen_df["word"].tolist()

            if dimension != "mixed":
                rng = random.Random(seed)
                rng.shuffle(chosen_words)
                exp2_words = chosen_words
            else:
                assert word_to_dim is not None
                d1, d2 = mixed_dimensions[0], mixed_dimensions[1]  # type: ignore[index]
                exp2_words = _reorder_words_to_alternate_dims(chosen_words, word_to_dim, d1, d2, seed)

                c1 = sum(1 for w in exp2_words if word_to_dim.get(w) == d1)
                c2 = sum(1 for w in exp2_words if word_to_dim.get(w) == d2)
                if abs(c1 - c2) > 1:
                    print(
                        f"[WARN] mixed exp2 subset is imbalanced: {d1}={c1}, {d2}={c2}. Strict alternation may be impossible; used best-effort alternation.",
                        file=sys.stderr,
                    )

    if which in ("exp2", "both"):
        exp2_jsonl_path = os.path.join(outdir, "exp2_sequential_raw.jsonl")
        exp2_csv_path = os.path.join(outdir, "exp2_sequential_raw.csv")

        exp2_kwargs = dict(
            out_jsonl_path=exp2_jsonl_path,
            out_csv_path=exp2_csv_path,
            resume=bool(cfg.get("exp2_resume", False)),
            context_window=cfg.get("exp2_context_window", None),
            compact_prompt=bool(cfg.get("exp2_compact_prompt", False)),
        )

        if dimension == "mixed":
            assert mixed_dimensions is not None
            d1, d2 = mixed_dimensions[0], mixed_dimensions[1]
            if word_to_dim is None:
                exp2_dims = _alternating_dims_for_length(len(exp2_words), d1, d2)
            else:
                exp2_dims = [word_to_dim.get(w, (d1 if (i % 2 == 0) else d2)) for i, w in enumerate(exp2_words)]
            exp2_result = runner.run_experiment2_sequential(exp2_words, dimensions=exp2_dims, **exp2_kwargs)
        else:
            exp2_result = runner.run_experiment2_sequential(exp2_words, **exp2_kwargs)

        save_jsonl(exp2_jsonl_path, exp2_result["raw"])
        save_csv_dicts(exp2_csv_path, exp2_result["raw"])

    if exp1_result is not None or exp2_result is not None:
        baseline_df = _build_baseline_df(sampled, dimension, mixed_dimensions, two_d_dimensions)

        if exp2_result is not None:
            exp2_words_order = [str(row["word"]) for row in exp2_result["raw"]]
            order_map = {w: i for i, w in enumerate(exp2_words_order)}
            baseline_df["__exp2_order"] = baseline_df["word"].astype(str).map(order_map)
            baseline_df = baseline_df[baseline_df["__exp2_order"].notna()].sort_values("__exp2_order").drop(columns=["__exp2_order"])

        merged = baseline_df

        if exp1_result is not None:
            exp1_sum_df = pd.DataFrame(exp1_result["summary"]).rename(columns={"asked_dimension": "exp1_dimension"})
            exp1_sum_df["word"] = exp1_sum_df["word"].astype(str)
            if "asked_emotion_type" in exp1_sum_df.columns:
                exp1_sum_df = exp1_sum_df.rename(columns={"asked_emotion_type": "exp1_emotion_type"})
            merged["word"] = merged["word"].astype(str)
            merged = merged.merge(exp1_sum_df, on="word", how="left", suffixes=("", "_exp1"))

        if exp2_result is not None:
            exp2_df = pd.DataFrame(exp2_result["raw"]).rename(columns={"rating": "exp2_rating", "asked_dimension": "exp2_dimension"})
            exp2_df["word"] = exp2_df["word"].astype(str)
            if "asked_emotion_type" in exp2_df.columns:
                exp2_df = exp2_df.rename(columns={"asked_emotion_type": "exp2_emotion_type"})
            merged["word"] = merged["word"].astype(str)
            keep_cols = [c for c in ["word", "exp2_rating", "exp2_dimension", "exp2_emotion_type"] if c in exp2_df.columns]
            merged = merged.merge(exp2_df[keep_cols], on="word", how="left")

        merged.to_csv(os.path.join(outdir, "combined_overview.csv"), index=False)

    print(f"Done. Outputs written to: {outdir}")


if __name__ == "__main__":
    main()
