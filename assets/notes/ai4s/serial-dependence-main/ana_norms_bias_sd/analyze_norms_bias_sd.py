# ana_norms_bias_sd/analyze_norms_bias_sd.py
import os
import json
import math
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import yaml  # PyYAML
except Exception as e:
    raise RuntimeError("Missing dependency: pyyaml. Please `pip install pyyaml`.") from e

try:
    from scipy.optimize import curve_fit
except Exception as e:
    raise RuntimeError("Missing dependency: scipy. Please `pip install scipy`.") from e


# -----------------------------
# emotion helpers
# -----------------------------
VALID_EMOTION_TYPES = (
    "anger",
    "anticipation",
    "disgust",
    "fear",
    "joy",
    "sadness",
    "surprise",
    "trust",
)


def normalize_emotion_type(emotion_type: Optional[str]) -> str:
    emo = str(emotion_type or "joy").strip().lower()
    if emo not in VALID_EMOTION_TYPES:
        raise ValueError(
            f"Unsupported emotion_type={emotion_type!r}. "
            f"Valid options: {', '.join(VALID_EMOTION_TYPES)}"
        )
    return emo


# -----------------------------
# paths / io
# -----------------------------
def _project_root_from_this_file() -> Path:
    # <root>/ana_norms_bias_sd/analyze_norms_bias_sd.py
    return Path(__file__).resolve().parents[1]


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def find_latest_run(outputs_dir: str) -> str:
    p = Path(outputs_dir)
    if not p.exists():
        raise FileNotFoundError(f"outputs_dir not found: {outputs_dir}")
    subdirs = [d for d in p.iterdir() if d.is_dir()]
    if not subdirs:
        raise FileNotFoundError(f"No run folders under: {outputs_dir}")
    subdirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return str(subdirs[0].resolve())


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        obj = yaml.safe_load(f) or {}
    return obj if isinstance(obj, dict) else {}


def load_run_config(run_dir: str) -> Dict[str, Any]:
    return load_yaml(Path(run_dir) / "run_config.yaml")


def load_exp2_df(run_dir: str) -> pd.DataFrame:
    """
    Prefer exp2_sequential_raw.csv because it preserves true trial order.
    Fallback to combined_overview.csv.
    """
    p1 = Path(run_dir) / "exp2_sequential_raw.csv"
    if p1.exists():
        df = pd.read_csv(p1)
        if "rating" in df.columns and "exp2_rating" not in df.columns:
            df = df.rename(columns={"rating": "exp2_rating"})
        if "asked_dimension" in df.columns and "exp2_dimension" not in df.columns:
            df = df.rename(columns={"asked_dimension": "exp2_dimension"})
        if "asked_emotion_type" in df.columns and "exp2_emotion_type" not in df.columns:
            df = df.rename(columns={"asked_emotion_type": "exp2_emotion_type"})
        df["word"] = df["word"].astype(str)
        df["exp2_rating"] = pd.to_numeric(df["exp2_rating"], errors="coerce")
        if "exp2_dimension" in df.columns:
            df["exp2_dimension"] = df["exp2_dimension"].astype(str)
        if "exp2_emotion_type" in df.columns:
            df["exp2_emotion_type"] = df["exp2_emotion_type"].astype(str)
        return df

    p2 = Path(run_dir) / "combined_overview.csv"
    if not p2.exists():
        raise FileNotFoundError(f"Missing exp2_sequential_raw.csv and combined_overview.csv under {run_dir}")
    df = pd.read_csv(p2)
    df["word"] = df["word"].astype(str)
    df["exp2_rating"] = pd.to_numeric(df.get("exp2_rating"), errors="coerce")
    if "exp2_dimension" in df.columns:
        df["exp2_dimension"] = df["exp2_dimension"].astype(str)
    if "exp2_emotion_type" in df.columns:
        df["exp2_emotion_type"] = df["exp2_emotion_type"].astype(str)
    return df


def load_exp1_summary_df(run_dir: str) -> pd.DataFrame:
    """
    Try exp1_isolated_summary.csv first; fallback to combined_overview.csv.
    Expected columns include:
      - word
      - mean
      - asked_dimension (or exp1_dimension in combined_overview)
    """
    p1 = Path(run_dir) / "exp1_isolated_summary.csv"
    if p1.exists():
        df = pd.read_csv(p1)
        if "word" not in df.columns:
            raise FileNotFoundError(f"Bad exp1_isolated_summary.csv (missing word): {p1}")
        if "mean" not in df.columns:
            raise FileNotFoundError(f"Bad exp1_isolated_summary.csv (missing mean): {p1}")
        if "asked_dimension" not in df.columns:
            if "exp1_dimension" in df.columns:
                df = df.rename(columns={"exp1_dimension": "asked_dimension"})
            else:
                df["asked_dimension"] = ""
        df["word"] = df["word"].astype(str)
        df["asked_dimension"] = df["asked_dimension"].astype(str)
        if "asked_emotion_type" in df.columns:
            df["asked_emotion_type"] = df["asked_emotion_type"].astype(str)
        df["mean"] = pd.to_numeric(df["mean"], errors="coerce")
        return df

    p2 = Path(run_dir) / "combined_overview.csv"
    if p2.exists():
        df = pd.read_csv(p2)
        if "word" not in df.columns or "mean" not in df.columns:
            raise FileNotFoundError("combined_overview.csv exists but missing word/mean; cannot do exp1 mode.")
        if "exp1_dimension" in df.columns and "asked_dimension" not in df.columns:
            df = df.rename(columns={"exp1_dimension": "asked_dimension"})
        if "exp1_emotion_type" in df.columns and "asked_emotion_type" not in df.columns:
            df = df.rename(columns={"exp1_emotion_type": "asked_emotion_type"})
        if "asked_dimension" not in df.columns:
            df["asked_dimension"] = ""
        df["word"] = df["word"].astype(str)
        df["asked_dimension"] = df["asked_dimension"].astype(str)
        if "asked_emotion_type" in df.columns:
            df["asked_emotion_type"] = df["asked_emotion_type"].astype(str)
        df["mean"] = pd.to_numeric(df["mean"], errors="coerce")

        dedup_cols = ["word", "asked_dimension"]
        if "asked_emotion_type" in df.columns:
            dedup_cols.append("asked_emotion_type")

        df = df.dropna(subset=["mean"]).drop_duplicates(subset=dedup_cols, keep="last")
        return df

    raise FileNotFoundError("Missing exp1_isolated_summary.csv and combined_overview.csv; cannot do exp1 mode.")


# -----------------------------
# DoG model and helpers
# -----------------------------
def dog_derivative(delta: np.ndarray, A: float, sigma: float) -> np.ndarray:
    sigma = max(float(sigma), 1e-9)
    return A * delta * np.exp(-0.5 * (delta / sigma) ** 2)


def dog_model(delta: np.ndarray, c0: float, A: float, sigma: float) -> np.ndarray:
    return c0 + dog_derivative(delta, A, sigma)


def half_amplitude(A: float, sigma: float) -> float:
    return float(abs(A) * abs(sigma) * math.exp(-0.5))


def compute_r2(y: np.ndarray, yhat: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    ss_res = float(np.nansum((y - yhat) ** 2))
    ss_tot = float(np.nansum((y - np.nanmean(y)) ** 2))
    if ss_tot <= 1e-12:
        return float("nan")
    return 1.0 - ss_res / ss_tot


def fit_dog(delta: np.ndarray, y: np.ndarray) -> Tuple[Tuple[float, float, float], float]:
    delta = np.asarray(delta, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(delta) & np.isfinite(y)
    if mask.sum() < 8:
        raise RuntimeError("Not enough finite points for DoG fit")

    d = delta[mask]
    yy = y[mask]

    c0_init = float(np.nanmean(yy))
    A_init = 0.05
    sigma_init = float(np.nanstd(d) if np.nanstd(d) > 1e-6 else 10.0)
    p0 = (c0_init, A_init, sigma_init)

    bounds_low = (-100.0, -10.0, 1e-3)
    bounds_high = (100.0, 10.0, 200.0)

    popt, _ = curve_fit(
        dog_model,
        d,
        yy,
        p0=p0,
        bounds=(bounds_low, bounds_high),
        maxfev=200000,
    )
    c0, A, sigma = [float(x) for x in popt]
    yhat = dog_model(d, c0, A, sigma)
    r2 = compute_r2(yy, yhat)
    return (c0, A, sigma), float(r2)


def permutation_test_half_amp(
    s: np.ndarray,
    prev: np.ndarray,
    resid: np.ndarray,
    half_amp_obs: float,
    n_perm: int,
    rng: np.random.Generator,
) -> Tuple[float, List[float]]:
    s = np.asarray(s, dtype=float)
    prev = np.asarray(prev, dtype=float)
    resid = np.asarray(resid, dtype=float)

    base_mask = np.isfinite(s) & np.isfinite(prev) & np.isfinite(resid)
    s0 = s[base_mask]
    prev0 = prev[base_mask]
    resid0 = resid[base_mask]

    null_vals: List[float] = []
    attempts = 0
    max_attempts = max(int(n_perm) * 5, 200)

    while len(null_vals) < int(n_perm) and attempts < max_attempts:
        attempts += 1
        prev_perm = rng.permutation(prev0)
        delta_perm = prev_perm - s0
        try:
            (c0, A, sigma), _ = fit_dog(delta_perm, resid0)
            null_vals.append(half_amplitude(A, sigma))
        except Exception:
            continue

    if not null_vals:
        return float("nan"), []

    obs = float(half_amp_obs)
    null = np.asarray(null_vals, dtype=float)
    p = (float(np.sum(null >= obs)) + 1.0) / (len(null) + 1.0)
    return float(p), null_vals


# -----------------------------
# plotting
# -----------------------------
def plot_error_vs_s(
    s: np.ndarray,
    e: np.ndarray,
    bias_meta: Dict[str, Any],
    out_path: Path,
    title: str,
) -> None:
    plt.figure(figsize=(6.0, 4.8), dpi=150)
    plt.scatter(s, e, s=14, alpha=0.45, label="error = resp - s")

    # overlay b_hat(s)
    if bias_meta.get("method") == "bin":
        centers = np.asarray(bias_meta["centers"], dtype=float)
        means = np.asarray(bias_meta["bin_means"], dtype=float)
        plt.plot(centers, means, lw=2, label="b_hat(s) (bin mean, smoothed)")
    elif bias_meta.get("method") == "poly" and bias_meta.get("coef") is not None:
        coef = np.asarray(bias_meta["coef"], dtype=float)
        p = np.poly1d(coef)
        xs = np.linspace(1.0, 100.0, 300)
        plt.plot(xs, p(xs), lw=2, label="b_hat(s) (poly)")
    elif bias_meta.get("method") in ("kernel", "knn_kernel") and bias_meta.get("curve_centers") is not None:
        xs = np.asarray(bias_meta["curve_centers"], dtype=float)
        ys = np.asarray(bias_meta["curve_values"], dtype=float)
        if xs.size > 0 and ys.size == xs.size:
            plt.plot(xs, ys, lw=2, label=f"b_hat(s) ({bias_meta.get('method')})")

    plt.axhline(0, lw=1, ls="--")
    plt.xlabel("s (stimulus value, 1–100)")
    plt.ylabel("error (resp - s)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_resid_vs_delta(
    delta: np.ndarray,
    resid: np.ndarray,
    c0: float,
    A: float,
    sigma: float,
    out_path: Path,
    title: str,
) -> None:
    xs = np.linspace(float(np.nanmin(delta)), float(np.nanmax(delta)), 400)
    ys = dog_model(xs, c0, A, sigma)

    plt.figure(figsize=(6.0, 4.8), dpi=150)
    plt.scatter(delta, resid, s=14, alpha=0.45, label="residual error e'")
    plt.plot(xs, ys, lw=2, label="fitted DoG")
    plt.axhline(0, lw=1, ls="--")
    plt.axvline(0, lw=1, ls="--")
    plt.xlabel("Δ = s[t-k] - s[t]")
    plt.ylabel("residual error e' (after removing b_hat(s))")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def _bin_mean_sem(x: np.ndarray, y: np.ndarray, n_bins: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size == 0:
        return np.array([]), np.array([]), np.array([]), np.array([])

    lo = float(np.nanmin(x))
    hi = float(np.nanmax(x))
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return np.array([]), np.array([]), np.array([]), np.array([])

    edges = np.linspace(lo, hi, int(max(2, n_bins)) + 1)
    idx = np.digitize(x, edges, right=False) - 1
    idx = np.clip(idx, 0, len(edges) - 2)

    centers = 0.5 * (edges[:-1] + edges[1:])
    means = np.full(len(centers), np.nan, dtype=float)
    sems = np.full(len(centers), np.nan, dtype=float)
    counts = np.zeros(len(centers), dtype=int)

    for b in range(len(centers)):
        m = (idx == b)
        counts[b] = int(m.sum())
        if counts[b] > 0:
            yy = y[m]
            means[b] = float(np.nanmean(yy))
            sd = float(np.nanstd(yy, ddof=1)) if counts[b] >= 2 else float("nan")
            sems[b] = sd / math.sqrt(counts[b]) if (counts[b] >= 2 and np.isfinite(sd)) else float("nan")

    return centers, means, sems, counts


def plot_resid_vs_delta_binned(
    delta: np.ndarray,
    resid: np.ndarray,
    c0: float,
    A: float,
    sigma: float,
    out_path: Path,
    title: str,
    n_bins: int = 25,
    min_count: int = 5,
) -> None:
    xs = np.linspace(float(np.nanmin(delta)), float(np.nanmax(delta)), 400)
    ys = dog_model(xs, c0, A, sigma)

    centers, means, sems, counts = _bin_mean_sem(delta, resid, n_bins=n_bins)
    if centers.size == 0:
        plot_resid_vs_delta(delta, resid, c0, A, sigma, out_path, title + "\n(bin failed; fallback raw)")
        return

    keep = counts >= int(max(1, min_count))
    centers2 = centers[keep]
    means2 = means[keep]
    sems2 = sems[keep]

    plt.figure(figsize=(6.0, 4.8), dpi=150)
    plt.scatter(delta, resid, s=10, alpha=0.20, label="raw e'")
    plt.errorbar(centers2, means2, yerr=sems2, fmt="o", capsize=2, label=f"binned mean±SEM (bins={n_bins})")
    plt.plot(xs, ys, lw=2, label="fitted DoG")
    plt.axhline(0, lw=1, ls="--")
    plt.axvline(0, lw=1, ls="--")
    plt.xlabel("Δ = s[t-k] - s[t]")
    plt.ylabel("residual error e'")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_halfamp_vs_k(summary: pd.DataFrame, out_path: Path, title: str) -> None:
    d = summary.dropna(subset=["k", "half_amp"]).copy()
    if d.empty:
        return

    d["k"] = d["k"].astype(int)
    d = d.sort_values("k")  # IMPORTANT: sort by k to avoid wrong connecting order
    ks = d["k"].to_numpy()
    amps = d["half_amp"].astype(float).to_numpy()
    ps = d["p_half_amp"].astype(float).to_numpy()

    plt.figure(figsize=(7.2, 4.8), dpi=150)
    plt.plot(ks, amps, marker="o", linewidth=2)
    plt.axhline(0, lw=1, ls="--")
    plt.xlabel("k (k-back; negative = future)")
    plt.ylabel("DoG half-amplitude |peak|")
    plt.title(title)
    plt.grid(True, alpha=0.3)

    for x, y, p in zip(ks, amps, ps):
        if np.isfinite(p):
            plt.annotate(f"p={p:.3g}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


# -----------------------------
# norms parsing + stimulus attach
# -----------------------------
_DIM_TO_PREFIX = {"valence": "V", "arousal": "A", "dominance": "D"}


def _canon_word(w: str) -> str:
    return str(w).strip().lower()


def load_warriner_norms(norms_csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(norms_csv_path)
    if "Word" in df.columns:
        df = df.rename(columns={"Word": "word"})
    elif "word" not in df.columns:
        df = df.rename(columns={df.columns[0]: "word"})
    df["word"] = df["word"].astype(str)
    df["word_key"] = df["word"].map(_canon_word)

    out = df[["word", "word_key"]].copy()

    for dim, pref in _DIM_TO_PREFIX.items():
        mean_sum = f"{pref}.Mean.Sum"
        sd_sum = f"{pref}.SD.Sum"
        mean_m = f"{pref}.Mean.M"
        mean_f = f"{pref}.Mean.F"

        for col in (mean_sum, sd_sum, mean_m, mean_f):
            if col not in df.columns:
                raise KeyError(f"Missing column in Warriner CSV: {col}")

        out[f"{dim}_mean_raw_1_9"] = pd.to_numeric(df[mean_sum], errors="coerce")
        out[f"{dim}_sd_sum"] = pd.to_numeric(df[sd_sum], errors="coerce")
        out[f"{dim}_mf_diff_raw_1_9"] = (
            pd.to_numeric(df[mean_m], errors="coerce") - pd.to_numeric(df[mean_f], errors="coerce")
        ).abs()

        out[f"{dim}_mean_1_100"] = 1.0 + (out[f"{dim}_mean_raw_1_9"] - 1.0) * (99.0 / 8.0)

    return out


def load_emotion_norms(norms_path: str) -> pd.DataFrame:
    p = Path(norms_path)
    suffix = p.suffix.lower()

    if suffix in (".txt", ".tsv"):
        df = pd.read_csv(
            norms_path,
            sep="\t",
            header=None,
            names=["word", "emotion", "emotion_score_raw_0_1"],
            comment="#",
            encoding="utf-8",
        )
    else:
        df = pd.read_csv(norms_path)

        col_map = {}
        cols_lower = {c.lower(): c for c in df.columns}

        if "word" in cols_lower:
            col_map[cols_lower["word"]] = "word"
        elif "term" in cols_lower:
            col_map[cols_lower["term"]] = "word"
        else:
            col_map[df.columns[0]] = "word"

        if "emotion" in cols_lower:
            col_map[cols_lower["emotion"]] = "emotion"
        elif "label" in cols_lower:
            col_map[cols_lower["label"]] = "emotion"

        score_candidates = [
            "emotion_score_raw_0_1",
            "score",
            "intensity",
            "value",
            "emotion_score",
        ]
        for cand in score_candidates:
            if cand in cols_lower:
                col_map[cols_lower[cand]] = "emotion_score_raw_0_1"
                break

        df = df.rename(columns=col_map)

        if "emotion_score_raw_0_1" not in df.columns:
            raise KeyError(
                "Emotion norms file must contain a score column, e.g. "
                "'emotion_score_raw_0_1' / 'score' / 'intensity'."
            )

    if "word" not in df.columns or "emotion" not in df.columns:
        raise KeyError("Emotion norms file must contain columns for word and emotion.")

    df["word"] = df["word"].astype(str).str.strip()
    df["emotion"] = df["emotion"].astype(str).str.strip().str.lower()
    df["emotion_score_raw_0_1"] = pd.to_numeric(df["emotion_score_raw_0_1"], errors="coerce")
    df = df.dropna(subset=["word", "emotion", "emotion_score_raw_0_1"]).copy()
    df = df[df["emotion"].isin(VALID_EMOTION_TYPES)].copy()

    df["word_key"] = df["word"].map(_canon_word)
    df["emotion_mean_1_100"] = 1.0 + 99.0 * df["emotion_score_raw_0_1"]

    return df[["word", "word_key", "emotion", "emotion_score_raw_0_1", "emotion_mean_1_100"]].drop_duplicates(
        ["word_key", "emotion"]
    )


def _decide_dim_used(exp2_df: pd.DataFrame, run_cfg: Dict[str, Any], params: Dict[str, Any]) -> pd.Series:
    dim_default = str(params.get("default_norm_dimension") or "").strip().lower()
    if not dim_default:
        dim_default = str(run_cfg.get("dimension", "valence")).strip().lower()
    if dim_default not in _DIM_TO_PREFIX:
        dim_default = "valence"

    if "exp2_dimension" in exp2_df.columns:
        dim_used = exp2_df["exp2_dimension"].astype(str).str.lower()
    else:
        dim_used = pd.Series([str(run_cfg.get("dimension", dim_default)).lower()] * len(exp2_df))

    dim_used = dim_used.where(dim_used.isin(list(_DIM_TO_PREFIX.keys())), other=dim_default)
    return dim_used


def attach_stimulus_values_norms(
    exp2_df: pd.DataFrame,
    norms_df: pd.DataFrame,
    run_cfg: Dict[str, Any],
    params: Dict[str, Any],
) -> pd.DataFrame:
    df = exp2_df.copy()
    df["word_key"] = df["word"].map(_canon_word)
    merged = df.merge(norms_df, on="word_key", how="left", suffixes=("", "_norm"))

    dim_used = _decide_dim_used(merged, run_cfg, params)
    merged["dim_used"] = dim_used

    s_raw = np.full(len(merged), np.nan, dtype=float)
    s_100 = np.full(len(merged), np.nan, dtype=float)

    for dim in _DIM_TO_PREFIX.keys():
        mask = (merged["dim_used"] == dim)
        s_raw_col = f"{dim}_mean_raw_1_9"
        s_100_col = f"{dim}_mean_1_100"
        if s_raw_col in merged.columns:
            s_raw[mask.values] = pd.to_numeric(merged.loc[mask, s_raw_col], errors="coerce").to_numpy(dtype=float)
        if s_100_col in merged.columns:
            s_100[mask.values] = pd.to_numeric(merged.loc[mask, s_100_col], errors="coerce").to_numpy(dtype=float)

    merged["s_raw_1_9"] = s_raw
    merged["s_1_100"] = s_100

    merged["exp2_rating"] = pd.to_numeric(merged["exp2_rating"], errors="coerce")
    merged["error"] = merged["exp2_rating"] - merged["s_1_100"]
    return merged


def attach_stimulus_values_emotion_norms(
    exp2_df: pd.DataFrame,
    norms_df: pd.DataFrame,
    run_cfg: Dict[str, Any],
    params: Dict[str, Any],
) -> pd.DataFrame:
    df = exp2_df.copy()
    df["word_key"] = df["word"].map(_canon_word)

    emo_default = normalize_emotion_type(
        params.get("default_emotion_type") or run_cfg.get("emotion_type") or "joy"
    )

    if "exp2_emotion_type" in df.columns:
        emo_used = df["exp2_emotion_type"].astype(str).str.strip().str.lower()
        emo_used = emo_used.where(emo_used.isin(VALID_EMOTION_TYPES), other=emo_default)
    else:
        emo_used = pd.Series([emo_default] * len(df), index=df.index)

    df["emotion_used"] = emo_used
    merged = df.merge(
        norms_df,
        left_on=["word_key", "emotion_used"],
        right_on=["word_key", "emotion"],
        how="left",
        suffixes=("", "_norm"),
    )

    merged["dim_used"] = "emotion"
    merged["s_raw_0_1"] = pd.to_numeric(merged["emotion_score_raw_0_1"], errors="coerce")
    merged["s_1_100"] = pd.to_numeric(merged["emotion_mean_1_100"], errors="coerce")
    merged["exp2_rating"] = pd.to_numeric(merged["exp2_rating"], errors="coerce")
    merged["error"] = merged["exp2_rating"] - merged["s_1_100"]
    return merged


def attach_stimulus_values_exp1(
    exp2_df: pd.DataFrame,
    exp1_sum_df: pd.DataFrame,
    run_cfg: Dict[str, Any],
    params: Dict[str, Any],
) -> pd.DataFrame:
    df = exp2_df.copy()
    df["word_key"] = df["word"].map(_canon_word)

    if "exp2_dimension" in df.columns:
        df["dim_used"] = df["exp2_dimension"].astype(str).str.lower()
    else:
        df["dim_used"] = str(run_cfg.get("dimension", "")).lower()

    if "exp2_emotion_type" in df.columns:
        emo_default = normalize_emotion_type(
            params.get("default_emotion_type") or run_cfg.get("emotion_type") or "joy"
        )
        df["exp2_emotion_type"] = (
            df["exp2_emotion_type"]
            .astype(str)
            .str.strip()
            .str.lower()
            .where(df["exp2_emotion_type"].astype(str).str.strip().str.lower().isin(VALID_EMOTION_TYPES), other=emo_default)
        )

    s1 = exp1_sum_df.copy()
    s1["word_key"] = s1["word"].map(_canon_word)
    s1["asked_dimension"] = s1.get("asked_dimension", "").astype(str).str.lower()
    if "asked_emotion_type" in s1.columns:
        s1["asked_emotion_type"] = s1["asked_emotion_type"].astype(str).str.strip().str.lower()
    s1["mean"] = pd.to_numeric(s1["mean"], errors="coerce")
    s1 = s1.dropna(subset=["mean"]).copy()

    has_exp1_emotion = "asked_emotion_type" in s1.columns and s1["asked_emotion_type"].astype(str).str.len().gt(0).any()
    has_exp2_emotion = "exp2_emotion_type" in df.columns and df["exp2_emotion_type"].astype(str).str.len().gt(0).any()

    if has_exp1_emotion and has_exp2_emotion:
        s1 = s1.rename(columns={"asked_dimension": "exp1_dim", "asked_emotion_type": "exp1_emotion_type", "mean": "exp1_mean"})
        merged = df.merge(
            s1[["word_key", "exp1_dim", "exp1_emotion_type", "exp1_mean"]],
            left_on=["word_key", "dim_used", "exp2_emotion_type"],
            right_on=["word_key", "exp1_dim", "exp1_emotion_type"],
            how="left",
        )

        miss = merged["exp1_mean"].isna()
        if miss.any():
            s1w = s1.drop_duplicates(subset=["word_key"], keep="last")[["word_key", "exp1_mean"]]
            merged.loc[miss, "exp1_mean"] = merged.loc[miss, "word_key"].map(
                dict(zip(s1w["word_key"], s1w["exp1_mean"]))
            )

    elif "asked_dimension" in s1.columns and s1["asked_dimension"].astype(str).str.len().gt(0).any():
        s1 = s1.rename(columns={"asked_dimension": "exp1_dim", "mean": "exp1_mean"})
        merged = df.merge(
            s1[["word_key", "exp1_dim", "exp1_mean"]],
            left_on=["word_key", "dim_used"],
            right_on=["word_key", "exp1_dim"],
            how="left",
        )
        miss = merged["exp1_mean"].isna()
        if miss.any():
            s1w = s1.drop_duplicates(subset=["word_key"], keep="last")[["word_key", "exp1_mean"]]
            merged.loc[miss, "exp1_mean"] = merged.loc[miss, "word_key"].map(
                dict(zip(s1w["word_key"], s1w["exp1_mean"]))
            )
    else:
        s1 = s1.rename(columns={"mean": "exp1_mean"})
        s1 = s1.drop_duplicates(subset=["word_key"], keep="last")
        merged = df.merge(s1[["word_key", "exp1_mean"]], on="word_key", how="left")

    merged["s_raw_1_9"] = np.nan
    merged["s_1_100"] = pd.to_numeric(merged["exp1_mean"], errors="coerce")
    merged["exp2_rating"] = pd.to_numeric(merged["exp2_rating"], errors="coerce")
    merged["error"] = merged["exp2_rating"] - merged["s_1_100"]
    return merged


# -----------------------------
# bias removal b(s)
# -----------------------------
def fit_bias_bin(
    s: np.ndarray,
    e: np.ndarray,
    n_bins: int,
    smooth_window: int = 1,
    s_min: float = 1.0,
    s_max: float = 100.0,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    s = np.asarray(s, dtype=float)
    e = np.asarray(e, dtype=float)

    n_bins = int(max(2, n_bins))
    edges = np.linspace(s_min, s_max, n_bins + 1)
    bin_idx = np.digitize(s, edges, right=False) - 1
    bin_idx = np.clip(bin_idx, 0, n_bins - 1)

    bin_means = np.full(n_bins, np.nan, dtype=float)
    bin_counts = np.zeros(n_bins, dtype=int)
    for b in range(n_bins):
        mask = (bin_idx == b) & np.isfinite(e) & np.isfinite(s)
        bin_counts[b] = int(mask.sum())
        if bin_counts[b] > 0:
            bin_means[b] = float(np.nanmean(e[mask]))

    w = int(max(1, smooth_window))
    if w > 1:
        sm = np.full_like(bin_means, np.nan, dtype=float)
        for i in range(n_bins):
            lo = max(0, i - w // 2)
            hi = min(n_bins, i + w // 2 + 1)
            window = bin_means[lo:hi]
            if np.isfinite(window).any():
                sm[i] = float(np.nanmean(window))
        bin_means = sm

    b_hat = bin_means[bin_idx]
    centers = 0.5 * (edges[:-1] + edges[1:])
    meta = {
        "method": "bin",
        "n_bins": n_bins,
        "smooth_window": w,
        "edges": edges.tolist(),
        "centers": centers.tolist(),
        "bin_means": bin_means.tolist(),
        "bin_counts": bin_counts.tolist(),
        "s_min": float(s_min),
        "s_max": float(s_max),
    }
    return b_hat, meta


def fit_bias_poly(s: np.ndarray, e: np.ndarray, degree: int) -> Tuple[np.ndarray, Dict[str, Any]]:
    s = np.asarray(s, dtype=float)
    e = np.asarray(e, dtype=float)
    degree = int(max(0, degree))

    mask = np.isfinite(s) & np.isfinite(e)
    if mask.sum() < (degree + 2):
        b_hat = np.full_like(s, np.nan, dtype=float)
        return b_hat, {"method": "poly", "degree": degree, "coef": None, "note": "not enough finite points"}

    coef = np.polyfit(s[mask], e[mask], degree)
    p = np.poly1d(coef)
    b_hat = p(s)
    return b_hat, {"method": "poly", "degree": degree, "coef": [float(x) for x in coef]}


def fit_bias_kernel(
    s: np.ndarray,
    e: np.ndarray,
    bandwidth: float = 8.0,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Fixed-bandwidth Gaussian kernel regression (Nadaraya–Watson).
    """
    s = np.asarray(s, dtype=float)
    e = np.asarray(e, dtype=float)
    mask = np.isfinite(s) & np.isfinite(e)
    s0 = s[mask]
    e0 = e[mask]

    if len(s0) < 10:
        b_hat = np.full_like(s, np.nan, dtype=float)
        return b_hat, {"method": "kernel", "bandwidth": float(bandwidth), "note": "not enough points"}

    h = float(max(bandwidth, 1e-6))
    diffs = (s[:, None] - s0[None, :]) / h
    W = np.exp(-0.5 * diffs * diffs)
    denom = np.sum(W, axis=1)
    numer = np.sum(W * e0[None, :], axis=1)
    b_hat = np.divide(numer, denom, out=np.full_like(numer, np.nan), where=(denom > 1e-12))

    xs = np.linspace(float(np.nanmin(s0)), float(np.nanmax(s0)), 200)
    diffs_x = (xs[:, None] - s0[None, :]) / h
    W_x = np.exp(-0.5 * diffs_x * diffs_x)
    denom_x = np.sum(W_x, axis=1)
    numer_x = np.sum(W_x * e0[None, :], axis=1)
    ys = np.divide(numer_x, denom_x, out=np.full_like(numer_x, np.nan), where=(denom_x > 1e-12))

    meta = {"method": "kernel", "bandwidth": float(h), "curve_centers": xs.tolist(), "curve_values": ys.tolist()}
    return b_hat, meta


def fit_bias_knn_kernel(
    s: np.ndarray,
    e: np.ndarray,
    k: int = 15,
    alpha: float = 1.0,
    min_bandwidth: float = 1e-3,
    curve_n: int = 200,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Adaptive-bandwidth Gaussian kernel regression (KNN bandwidth) a.k.a. "scheme B1".
    """
    s = np.asarray(s, dtype=float)
    e = np.asarray(e, dtype=float)

    mask = np.isfinite(s) & np.isfinite(e)
    if mask.sum() == 0:
        return np.full_like(s, np.nan, dtype=float), {
            "method": "knn_kernel",
            "k": int(k),
            "alpha": float(alpha),
            "note": "no finite points",
        }

    s0 = s[mask]
    e0 = e[mask]
    n = int(len(s0))

    k = int(max(1, k))
    kth_index = min(k - 1, n - 1)

    dist = np.abs(s0[:, None] - s0[None, :])
    dist.sort(axis=1)
    d_k = dist[:, kth_index]
    h = float(alpha) * np.maximum(d_k, float(min_bandwidth))

    diffs = (s0[:, None] - s0[None, :]) / h[:, None]
    W = np.exp(-0.5 * diffs * diffs)
    denom = W.sum(axis=1)
    numer = (W * e0[None, :]).sum(axis=1)
    b0 = np.divide(numer, denom, out=np.full_like(numer, np.nan), where=(denom > 1e-12))

    w2 = (W * W).sum(axis=1)
    neff = np.divide(denom * denom, w2, out=np.full_like(denom, np.nan), where=(w2 > 1e-12))

    b_hat = np.full_like(s, np.nan, dtype=float)
    b_hat[mask] = b0

    s_min = float(np.nanmin(s0))
    s_max = float(np.nanmax(s0))
    curve_n = int(max(20, curve_n))
    xs = np.linspace(s_min, s_max, curve_n)

    dist_x = np.abs(xs[:, None] - s0[None, :])
    dist_x.sort(axis=1)
    dk_x = dist_x[:, kth_index]
    h_x = float(alpha) * np.maximum(dk_x, float(min_bandwidth))
    diffs_x = (xs[:, None] - s0[None, :]) / h_x[:, None]
    W_x = np.exp(-0.5 * diffs_x * diffs_x)
    denom_x = W_x.sum(axis=1)
    numer_x = (W_x * e0[None, :]).sum(axis=1)
    ys = np.divide(numer_x, denom_x, out=np.full_like(numer_x, np.nan), where=(denom_x > 1e-12))

    meta = {
        "method": "knn_kernel",
        "k": int(k),
        "alpha": float(alpha),
        "min_bandwidth": float(min_bandwidth),
        "n_points": int(n),
        "bandwidth_min": float(np.nanmin(h)),
        "bandwidth_median": float(np.nanmedian(h)),
        "bandwidth_max": float(np.nanmax(h)),
        "neff_min": float(np.nanmin(neff)),
        "neff_median": float(np.nanmedian(neff)),
        "neff_max": float(np.nanmax(neff)),
        "curve_centers": xs.tolist(),
        "curve_values": ys.tolist(),
    }
    return b_hat, meta


# -----------------------------
# main
# -----------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Remove b(s) then DoG serial dependence on residuals (norms or exp1 s).")
    ap.add_argument("--outputs-dir", type=str, default="outputs")
    ap.add_argument("--run-dir", type=str, default=None, help="Default: latest under outputs-dir")
    ap.add_argument("--config", type=str, default=None, help="Default: ana_norms_bias_sd/params.yaml")
    ap.add_argument("--k", type=int, default=None, help="Run a single k-back (optional)")
    ap.add_argument("--n-perm", type=int, default=None)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--exp1", action="store_true", help="Use Exp1 mean as stimulus value s (emotion-only).")
    args = ap.parse_args()

    this_dir = Path(__file__).resolve().parent
    root = _project_root_from_this_file()

    cfg_path = Path(args.config) if args.config else (this_dir / "params.yaml")
    params = load_yaml(cfg_path)

    k_values = params.get("k_values", [1, 2, 3, 5, -1, -2, -3, -5])
    n_perm = int(args.n_perm if args.n_perm is not None else params.get("n_permutations", 1000))
    seed = int(args.seed if args.seed is not None else params.get("random_seed", 123))
    make_scatter_all = bool(params.get("make_scatter_for_all_k", False))

    # delta bin plot params
    delta_bins = int(params.get("delta_bin_n_bins", 25))
    delta_min_count = int(params.get("delta_bin_min_count", 5))

    run_dir = args.run_dir or find_latest_run(args.outputs_dir)
    run_tag = Path(run_dir).name
    run_cfg = load_run_config(run_dir)

    exp2_df = load_exp2_df(run_dir)

    run_dimension = str(run_cfg.get("dimension", "")).strip().lower()
    use_exp1_effective = bool(args.exp1 and run_dimension == "emotion")

    if use_exp1_effective:
        stimulus_source = "exp1_mean"
        exp1_sum = load_exp1_summary_df(run_dir)
        merged = attach_stimulus_values_exp1(exp2_df, exp1_sum, run_cfg, params)
        norms_path = None
        raw_min = float("nan")
        raw_max = float("nan")
    else:
        if run_dimension == "emotion":
            stimulus_source = "emotion_human_norms"
            norms_default = params.get(
                "emotion_norms_path",
                run_cfg.get("excel_path", params.get("norms_csv_path", "testing_data/NRC-Emotion-Intensity-Lexicon-v1.txt")),
            )
            norms_path = Path(str(norms_default))
            if not norms_path.is_absolute():
                norms_path = (root / norms_path).resolve()
            if not norms_path.exists():
                raise FileNotFoundError(f"Emotion norms file not found: {norms_path}")

            norms_df = load_emotion_norms(str(norms_path))
            merged = attach_stimulus_values_emotion_norms(exp2_df, norms_df, run_cfg, params)

            merged2 = merged.dropna(subset=["s_raw_0_1"]).copy()
            raw_min = float(np.nanmin(merged2["s_raw_0_1"].to_numpy(dtype=float))) if len(merged2) else float("nan")
            raw_max = float(np.nanmax(merged2["s_raw_0_1"].to_numpy(dtype=float))) if len(merged2) else float("nan")
        else:
            stimulus_source = "warriner_norms"
            norms_csv_path = str(params.get("norms_csv_path", "testing_data/Warriner_et_alemotratings.csv"))
            norms_path = Path(norms_csv_path)
            if not norms_path.is_absolute():
                norms_path = (root / norms_path).resolve()
            if not norms_path.exists():
                raise FileNotFoundError(f"Norms CSV not found: {norms_path}")

            norms_df = load_warriner_norms(str(norms_path))
            merged = attach_stimulus_values_norms(exp2_df, norms_df, run_cfg, params)

            merged2 = merged.dropna(subset=["s_raw_1_9"]).copy()
            raw_min = float(np.nanmin(merged2["s_raw_1_9"].to_numpy(dtype=float))) if len(merged2) else float("nan")
            raw_max = float(np.nanmax(merged2["s_raw_1_9"].to_numpy(dtype=float))) if len(merged2) else float("nan")

    merged["exp2_rating"] = pd.to_numeric(merged["exp2_rating"], errors="coerce")
    merged["s_1_100"] = pd.to_numeric(merged["s_1_100"], errors="coerce")
    merged["error"] = pd.to_numeric(merged["error"], errors="coerce")
    merged = merged.dropna(subset=["exp2_rating", "s_1_100", "error"]).reset_index(drop=True)

    # bias removal
    bias_method = str(params.get("bias_method", "bin")).strip().lower()
    s = merged["s_1_100"].to_numpy(dtype=float)
    e = merged["error"].to_numpy(dtype=float)

    if bias_method == "poly":
        degree = int(params.get("poly_degree", 3))
        b_hat, bias_meta = fit_bias_poly(s, e, degree=degree)
    elif bias_method == "kernel":
        bw = float(params.get("kernel_bandwidth", 8.0))
        b_hat, bias_meta = fit_bias_kernel(s, e, bandwidth=bw)
    elif bias_method in ("knn_kernel", "knn"):
        knn_k = int(params.get("knn_k", 15))
        knn_alpha = float(params.get("knn_alpha", 1.0))
        knn_min_bw = float(params.get("knn_min_bandwidth", 1e-3))
        knn_curve_n = int(params.get("knn_curve_n", 200))
        b_hat, bias_meta = fit_bias_knn_kernel(
            s,
            e,
            k=knn_k,
            alpha=knn_alpha,
            min_bandwidth=knn_min_bw,
            curve_n=knn_curve_n,
        )
    else:
        n_bins = int(params.get("n_bins", 30))
        smooth_w = int(params.get("bin_smooth_window", 1))
        b_hat, bias_meta = fit_bias_bin(s, e, n_bins=n_bins, smooth_window=smooth_w, s_min=1.0, s_max=100.0)

    merged["b_hat"] = b_hat
    merged["resid"] = merged["error"] - merged["b_hat"]

    # results folder: keep original behavior, but only emotion+--exp1 goes to __exp1
    out_tag = f"{run_tag}__exp1" if use_exp1_effective else run_tag
    results_root = this_dir / "results" / out_tag
    ensure_dir(results_root)

    # save bias meta
    bias_info = {
        "run_tag": run_tag,
        "out_tag": out_tag,
        "stimulus_source": stimulus_source,
        "norms_csv": str(norms_path) if norms_path is not None else None,
        "raw_scale_min_observed": raw_min,
        "raw_scale_max_observed": raw_max,
        "bias_method": bias_method,
        "bias_meta": bias_meta,
        "match_n": int(len(merged)),
        "match_rate_vs_exp2": float(len(merged) / max(len(exp2_df), 1)),
    }
    with open(results_root / "bias_fit.json", "w", encoding="utf-8") as f:
        json.dump(bias_info, f, ensure_ascii=False, indent=2)

    ks = [int(args.k)] if args.k is not None else [int(k) for k in k_values]
    rng = np.random.default_rng(seed)

    summary_rows: List[Dict[str, Any]] = []
    fit_json: Dict[str, Any] = {
        "run_tag": run_tag,
        "out_tag": out_tag,
        "stimulus_source": stimulus_source,
        "seed": seed,
        "n_perm": n_perm,
        "bias_method": bias_method,
        "raw_scale_min_observed": raw_min,
        "raw_scale_max_observed": raw_max,
        "results": [],
    }

    for k in ks:
        d = merged.copy()
        d["prev_s"] = d["s_1_100"].shift(k)
        d["delta"] = d["prev_s"] - d["s_1_100"]

        dk = d.dropna(subset=["s_1_100", "prev_s", "delta", "resid"]).reset_index(drop=True)
        if len(dk) < 8:
            row = {
                "k": int(k),
                "n": int(len(dk)),
                "c0": np.nan,
                "A": np.nan,
                "sigma": np.nan,
                "r2": np.nan,
                "half_amp": np.nan,
                "p_half_amp": np.nan,
            }
            summary_rows.append(row)
            fit_json["results"].append({**row, "null_half_amp": None})
            continue

        delta = dk["delta"].to_numpy(dtype=float)
        resid = dk["resid"].to_numpy(dtype=float)
        s_cur = dk["s_1_100"].to_numpy(dtype=float)
        prev_s = dk["prev_s"].to_numpy(dtype=float)

        (c0, A, sigma), r2 = fit_dog(delta, resid)
        ha = half_amplitude(A, sigma)

        p, null = permutation_test_half_amp(
            s=s_cur,
            prev=prev_s,
            resid=resid,
            half_amp_obs=ha,
            n_perm=n_perm,
            rng=rng,
        )

        row = {
            "k": int(k),
            "n": int(len(dk)),
            "c0": float(c0),
            "A": float(A),
            "sigma": float(sigma),
            "r2": float(r2),
            "half_amp": float(ha),
            "p_half_amp": float(p),
        }
        summary_rows.append(row)
        fit_json["results"].append({**row, "null_half_amp": null})

        if (k == 1) or make_scatter_all:
            title1 = (
                f"error vs s (run={run_tag})\n"
                f"stimulus={stimulus_source} ; bias={bias_method}"
                + (f" ; raw scale observed: [{raw_min:.3g}, {raw_max:.3g}]" if np.isfinite(raw_min) else "")
            )
            plot_error_vs_s(
                s=merged["s_1_100"].to_numpy(dtype=float),
                e=merged["error"].to_numpy(dtype=float),
                bias_meta=bias_meta,
                out_path=results_root / ("e_vs_s_k1.png" if k == 1 else f"e_vs_s_k{k}.png"),
                title=title1,
            )

            title2 = f"residual e' vs Δ (k={k}) (run={run_tag})\nDoG fit + permutation p"
            plot_resid_vs_delta(
                delta=delta,
                resid=resid,
                c0=c0,
                A=A,
                sigma=sigma,
                out_path=results_root / ("e_resid_vs_delta_k1.png" if k == 1 else f"e_resid_vs_delta_k{k}.png"),
                title=title2,
            )

            title3 = f"binned mean of residual e' vs Δ (k={k}) (run={run_tag})\nmean±SEM + DoG"
            plot_resid_vs_delta_binned(
                delta=delta,
                resid=resid,
                c0=c0,
                A=A,
                sigma=sigma,
                out_path=results_root / ("e_resid_bin_vs_delta_k1.png" if k == 1 else f"e_resid_bin_vs_delta_k{k}.png"),
                title=title3,
                n_bins=delta_bins,
                min_count=delta_min_count,
            )

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(results_root / "nback_summary.csv", index=False, encoding="utf-8")

    with open(results_root / ("fit_k.json" if len(ks) == 1 else "fit_all_k.json"), "w", encoding="utf-8") as f:
        json.dump(fit_json, f, ensure_ascii=False, indent=2)

    plot_halfamp_vs_k(
        summary=summary_df,
        out_path=results_root / "halfamp_vs_k.png",
        title=f"DoG half-amplitude vs k (run={run_tag}) [{stimulus_source}]",
    )

    print("Done.")
    print("Run:", run_tag)
    print("Stimulus:", stimulus_source)
    print("Bias method:", bias_method)
    print("Results:", results_root)


if __name__ == "__main__":
    main()