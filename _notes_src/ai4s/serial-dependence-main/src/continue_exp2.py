# src/continue_exp2.py
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

import pandas as pd
import yaml

from api_client import DMXClient
from prompts import SYSTEM_PROMPT, build_user_prompt, normalize_emotion_type
from experiment import ExperimentRunner
from utils import save_csv_dicts


def load_yaml(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        obj = yaml.safe_load(f) or {}
    return obj if isinstance(obj, dict) else {}


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def append_jsonl(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()


def replay_messages_from_raw(raw_rows: List[Dict[str, Any]], default_dim: str, emotion_type: str) -> List[Dict[str, str]]:
    msgs: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for r in raw_rows:
        w = str(r["word"])
        dim = str(r.get("asked_dimension") or default_dim)
        user_prompt = build_user_prompt(w, dim, emotion_type=emotion_type)
        msgs.append({"role": "user", "content": user_prompt})
        msgs.append({"role": "assistant", "content": str(r.get("text") or "")})
    return msgs


def build_combined_overview(run_dir: str) -> None:
    sampled_path = os.path.join(run_dir, "sampled_words.csv")
    exp1_sum_path = os.path.join(run_dir, "exp1_isolated_summary.csv")
    exp2_csv_path = os.path.join(run_dir, "exp2_sequential_raw.csv")
    out_path = os.path.join(run_dir, "combined_overview.csv")

    if not os.path.exists(sampled_path):
        raise FileNotFoundError(f"Missing: {sampled_path}")
    if not os.path.exists(exp2_csv_path):
        raise FileNotFoundError(f"Missing: {exp2_csv_path}")

    sampled = pd.read_csv(sampled_path)
    sampled["word"] = sampled["word"].astype(str)

    if "chatgpt_concreteness_estimate" in sampled.columns:
        base = sampled[["word", "chatgpt_concreteness_estimate"]].rename(
            columns={"chatgpt_concreteness_estimate": "baseline_excel_col6"}
        )
    elif "emotion_mean_1_100" in sampled.columns:
        base = sampled[["word", "emotion_mean_1_100"]].rename(columns={"emotion_mean_1_100": "baseline_excel_col6"})
    else:
        base = sampled[["word"]].copy()
        base["baseline_excel_col6"] = pd.NA

    exp2 = pd.read_csv(exp2_csv_path)
    exp2["word"] = exp2["word"].astype(str)
    exp2 = exp2.rename(columns={"rating": "exp2_rating", "asked_dimension": "exp2_dimension", "asked_emotion_type": "exp2_emotion_type"})
    exp2_words_order = exp2["word"].tolist()
    order_map = {w: i for i, w in enumerate(exp2_words_order)}

    base["__exp2_order"] = base["word"].map(order_map)
    base = base[base["__exp2_order"].notna()].sort_values("__exp2_order").drop(columns=["__exp2_order"])

    keep_cols = [c for c in ["word", "exp2_rating", "exp2_dimension", "exp2_emotion_type"] if c in exp2.columns]
    merged = base.merge(exp2[keep_cols], on="word", how="left")

    if os.path.exists(exp1_sum_path):
        exp1_sum = pd.read_csv(exp1_sum_path)
        exp1_sum["word"] = exp1_sum["word"].astype(str)
        exp1_sum = exp1_sum.rename(columns={"asked_dimension": "exp1_dimension", "asked_emotion_type": "exp1_emotion_type"})
        merged = merged.merge(exp1_sum, on="word", how="left", suffixes=("", "_exp1"))

    merged.to_csv(out_path, index=False)
    print(f"[OK] combined_overview.csv written: {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True, help="e.g. outputs/<run_tag>")
    ap.add_argument("--config", default="config.yaml", help="project config.yaml (for api_key etc.)")
    ap.add_argument("--api_key", default=None)
    ap.add_argument("--base_url", default=None)
    ap.add_argument("--resume", action="store_true", help="resume from existing exp2_sequential_raw.jsonl if present")
    args = ap.parse_args()

    run_dir = args.run_dir
    if not os.path.isdir(run_dir):
        raise FileNotFoundError(f"run-dir not found: {run_dir}")

    run_cfg = load_yaml(os.path.join(run_dir, "run_config.yaml"))
    file_cfg = load_yaml(args.config)

    base_url = args.base_url or run_cfg.get("base_url") or file_cfg.get("base_url") or "https://www.dmxapi.cn/v1"
    api_key = args.api_key or file_cfg.get("api_key")
    if not api_key:
        raise RuntimeError("api_key is required. Put it in config.yaml or pass --api_key.")

    model = run_cfg.get("model", file_cfg.get("model", "gpt-4o-mini"))
    temperature = float(run_cfg.get("temperature", file_cfg.get("temperature", 0.0)))
    dimension = str(run_cfg.get("dimension", "concreteness"))
    emotion_type = normalize_emotion_type(run_cfg.get("emotion_type", "joy"))

    sampled_path = os.path.join(run_dir, "sampled_words.csv")
    if not os.path.exists(sampled_path):
        raise FileNotFoundError(f"Missing: {sampled_path}")

    sampled = pd.read_csv(sampled_path)
    words = sampled["word"].astype(str).tolist()
    exp2_words = list(words)

    exp2_jsonl = os.path.join(run_dir, "exp2_sequential_raw.jsonl")
    exp2_csv = os.path.join(run_dir, "exp2_sequential_raw.csv")

    raw_rows: List[Dict[str, Any]] = []
    if args.resume and os.path.exists(exp2_jsonl):
        raw_rows = read_jsonl(exp2_jsonl)
        ok_prefix = True
        for i, r in enumerate(raw_rows):
            if i >= len(exp2_words):
                break
            if str(r.get("word")) != str(exp2_words[i]):
                ok_prefix = False
                break
        if not ok_prefix:
            print("[WARN] Existing JSONL does not match current exp2_words order. Will resume by count anyway.", file=sys.stderr)

    start_i = len(raw_rows)
    if start_i >= len(exp2_words):
        print("[OK] Exp2 already complete (nothing to do).")
    else:
        print(f"[INFO] Exp2 resume: {start_i}/{len(exp2_words)} done. Continuing...")

        client = DMXClient(base_url=base_url, api_key=api_key)
        runner = ExperimentRunner(
            client=client,
            model=str(model),
            temperature=temperature,
            logs_dir=os.path.join(os.getcwd(), "logs"),
            ci95_enable=False,
            ci95_threshold=0.0,
            max_trials_per_word=1,
            rating_dimension=dimension,
            emotion_type=emotion_type,
        )

        messages = replay_messages_from_raw(raw_rows, default_dim=dimension, emotion_type=emotion_type)

        for i in range(start_i, len(exp2_words)):
            w = exp2_words[i]
            asked_dim = dimension
            user_prompt = build_user_prompt(w, asked_dim, emotion_type=emotion_type)
            messages.append({"role": "user", "content": user_prompt})

            content = client.chat_completion(str(model), messages, temperature)
            rating = runner._parse_rating_int_1_100(content)

            row = {"trial": i + 1, "word": w, "rating": rating, "text": content, "asked_dimension": asked_dim}
            if asked_dim == "emotion":
                row["asked_emotion_type"] = emotion_type
            raw_rows.append(row)
            append_jsonl(exp2_jsonl, row)
            messages.append({"role": "assistant", "content": content})

            if (i + 1) % 25 == 0:
                print(f"[INFO] progress {i+1}/{len(exp2_words)}")

    save_csv_dicts(exp2_csv, raw_rows)
    print(f"[OK] exp2 CSV written: {exp2_csv}")
    build_combined_overview(run_dir)


if __name__ == "__main__":
    main()
