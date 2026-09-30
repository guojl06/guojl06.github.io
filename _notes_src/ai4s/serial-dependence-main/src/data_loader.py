# data_loader.py
import os
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd

from prompts import VALID_EMOTION_TYPES, normalize_emotion_type


_DIM_TO_PREFIX = {"valence": "V", "arousal": "A", "dominance": "D"}


def load_and_clean_excel(path: str) -> pd.DataFrame:
    """
    Legacy loader:
      - first column = word
      - sixth column = chatgpt_concreteness_estimate
    """
    df = pd.read_excel(path, header=0, engine="openpyxl")
    words = df.iloc[:, 0].astype(str).rename("word")
    chatgpt_col = df.iloc[:, 5].rename("chatgpt_concreteness_estimate")
    clean = pd.concat([words, chatgpt_col], axis=1)
    clean = clean.dropna(subset=["chatgpt_concreteness_estimate"]).reset_index(drop=True)
    return clean


def _canon_word(w: str) -> str:
    return str(w).strip().lower()


def _require_col(df: pd.DataFrame, col: str) -> None:
    if col not in df.columns:
        raise KeyError(f"Missing column: {col}")


def load_warriner_vad_csv(path: str) -> pd.DataFrame:
    """
    Load Warriner_et_alemotratings.csv and produce standardized columns:
      word, word_key,
      valence_mean_raw_1_9, valence_mean_1_100, valence_sd_sum, valence_mf_diff_raw_1_9,
      arousal_..., dominance_...
    """
    df = pd.read_csv(path)

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

        _require_col(df, mean_sum)
        _require_col(df, sd_sum)
        _require_col(df, mean_m)
        _require_col(df, mean_f)

        out[f"{dim}_mean_raw_1_9"] = pd.to_numeric(df[mean_sum], errors="coerce")
        out[f"{dim}_sd_sum"] = pd.to_numeric(df[sd_sum], errors="coerce")

        mm = pd.to_numeric(df[mean_m], errors="coerce")
        mf = pd.to_numeric(df[mean_f], errors="coerce")
        out[f"{dim}_mf_diff_raw_1_9"] = (mm - mf).abs()

        # 1-9 -> 1-100
        out[f"{dim}_mean_1_100"] = 1.0 + (out[f"{dim}_mean_raw_1_9"] - 1.0) * (99.0 / 8.0)

    return out


def load_nrc_emotion_intensity_txt(path: str) -> pd.DataFrame:
    """
    Load NRC-Emotion-Intensity-Lexicon-v1.txt and produce standardized columns:
      word, word_key, emotion, emotion_score_raw_0_1, emotion_mean_1_100
    """
    df = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=["word", "emotion", "emotion_score_raw_0_1"],
        comment="#",
        encoding="utf-8",
    )

    df["word"] = df["word"].astype(str).str.strip()
    df["emotion"] = df["emotion"].astype(str).str.strip().str.lower()
    df["emotion_score_raw_0_1"] = pd.to_numeric(df["emotion_score_raw_0_1"], errors="coerce")
    df = df.dropna(subset=["word", "emotion", "emotion_score_raw_0_1"]).copy()
    df = df[df["emotion"].isin(VALID_EMOTION_TYPES)].copy()

    df["word_key"] = df["word"].map(_canon_word)
    df["emotion_mean_1_100"] = 1.0 + 99.0 * df["emotion_score_raw_0_1"]

    # per (word, emotion) keep first, though file should already be unique
    df = df.drop_duplicates(subset=["word_key", "emotion"], keep="first").reset_index(drop=True)
    return df[["word", "word_key", "emotion", "emotion_score_raw_0_1", "emotion_mean_1_100"]]


def filter_warriner_words(
    df: pd.DataFrame,
    dims: List[str],
    max_sd_sum: float = 1.7,
    max_mf_diff: float = 0.5,
) -> pd.DataFrame:
    d = df.copy()

    dims2 = []
    for x in dims:
        xx = str(x).strip().lower()
        if xx in _DIM_TO_PREFIX:
            dims2.append(xx)
        else:
            raise ValueError(f"Warriner VAD supports only {list(_DIM_TO_PREFIX.keys())}, got dim={x}")

    for dim in dims2:
        sd_col = f"{dim}_sd_sum"
        mf_col = f"{dim}_mf_diff_raw_1_9"
        if sd_col not in d.columns or mf_col not in d.columns:
            raise KeyError(f"Missing required columns for dim={dim}: {sd_col}, {mf_col}")

        d = d.dropna(subset=[sd_col, mf_col]).copy()
        d = d[(d[sd_col] < float(max_sd_sum)) & (d[mf_col] <= float(max_mf_diff))].copy()

    d = d.reset_index(drop=True)
    return d


def filter_nrc_emotion_words(df: pd.DataFrame, emotion_type: str) -> pd.DataFrame:
    emo = normalize_emotion_type(emotion_type)
    d = df.copy()
    d = d[d["emotion"].astype(str).str.lower() == emo].copy()
    d = d.dropna(subset=["emotion_score_raw_0_1", "emotion_mean_1_100"]).reset_index(drop=True)
    return d


def load_word_source(
    path: str,
    dims_for_warriner: Optional[List[str]] = None,
    warriner_max_sd_sum: float = 1.7,
    warriner_max_mf_diff: float = 0.5,
    emotion_type: str = "joy",
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Unified loader:
      - .xlsx -> legacy excel loader (word + chatgpt_concreteness_estimate)
      - Warriner .csv -> load + filter + return norms columns
      - NRC Emotion Intensity .txt -> load one target emotion and return norm columns

    Returns (df, meta).
    """
    meta: Dict[str, Any] = {"source_path": path}

    if path.lower().endswith(".xlsx"):
        df = load_and_clean_excel(path)
        meta.update(
            {
                "source_type": "excel_concreteness",
                "value_cols": ["chatgpt_concreteness_estimate"],
            }
        )
        return df, meta

    fname = os.path.basename(path).lower()
    if path.lower().endswith(".csv") and ("warriner" in fname or "emotratings" in fname):
        if not dims_for_warriner:
            raise ValueError("dims_for_warriner is required when using Warriner CSV.")
        df0 = load_warriner_vad_csv(path)
        df = filter_warriner_words(
            df0,
            dims=dims_for_warriner,
            max_sd_sum=warriner_max_sd_sum,
            max_mf_diff=warriner_max_mf_diff,
        )
        meta.update(
            {
                "source_type": "warriner_vad",
                "filters": {
                    "max_sd_sum": float(warriner_max_sd_sum),
                    "max_mf_diff": float(warriner_max_mf_diff),
                    "dims_applied": [str(x).lower() for x in dims_for_warriner],
                },
                "stimulus_col_by_dim": {
                    "valence": "valence_mean_1_100",
                    "arousal": "arousal_mean_1_100",
                    "dominance": "dominance_mean_1_100",
                },
            }
        )
        return df, meta

    if path.lower().endswith(".txt") and "emotion-intensity-lexicon" in fname:
        emo = normalize_emotion_type(emotion_type)
        df0 = load_nrc_emotion_intensity_txt(path)
        df = filter_nrc_emotion_words(df0, emotion_type=emo)
        meta.update(
            {
                "source_type": "nrc_emotion_intensity",
                "emotion_type": emo,
                "stimulus_col_by_dim": {"emotion": "emotion_mean_1_100"},
                "raw_score_col": "emotion_score_raw_0_1",
            }
        )
        return df, meta

    raise ValueError(
        f"Unsupported word source: {path} "
        "(supported: legacy .xlsx, Warriner .csv, NRC-Emotion-Intensity-Lexicon-v1.txt)."
    )
