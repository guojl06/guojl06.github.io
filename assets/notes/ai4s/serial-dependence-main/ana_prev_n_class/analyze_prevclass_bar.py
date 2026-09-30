# ana_prev_n_class/analyze_prevclass_bar.py
from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# matplotlib 用于画 delta-n 图
import matplotlib.pyplot as plt

try:
    import yaml  # pyyaml
except Exception as e:
    yaml = None

# scipy 可选：用于 Welch t-test
try:
    from scipy import stats as scipy_stats  # type: ignore
except Exception:
    scipy_stats = None


# ----------------------------
# Config / IO helpers
# ----------------------------
def load_yaml(path: Path) -> Dict:
    if yaml is None:
        raise RuntimeError("pyyaml 未安装，无法读取 YAML 参数文件。请 pip install pyyaml")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _is_probably_exp2_csv(p: Path) -> bool:
    name = p.name.lower()
    if not name.endswith(".csv"):
        return False
    if "exp2" not in name:
        return False
    # 排除明显不是序列 trial 的汇总
    if "overview" in name or "combined" in name or "summary" in name:
        return False
    return True


def find_exp2_csv(run_dir: Path) -> Path:
    """
    尝试在 run_dir 下自动定位 Exp2 的序列数据 CSV。
    若你的项目 Exp2 文件命名不同，建议用 --exp2_csv 显式指定。
    """
    candidates = [p for p in run_dir.rglob("*.csv") if _is_probably_exp2_csv(p)]
    if not candidates:
        # 兜底：含 exp2 的任何 csv
        candidates = [p for p in run_dir.rglob("*.csv") if "exp2" in p.name.lower()]

    if not candidates:
        raise FileNotFoundError(
            f"在 {run_dir} 下未找到 Exp2 CSV。请用 --exp2_csv 显式指定 Exp2 数据文件路径。"
        )

    def score(p: Path) -> Tuple[int, int]:
        n = p.name.lower()
        pri = 0
        if "raw" in n:
            pri -= 30
        if "trial" in n or "trials" in n:
            pri -= 20
        if "result" in n or "results" in n:
            pri -= 10
        # 更深的路径通常更像中间产物，略微加权；这里反过来让“更靠近 run_dir 根部”的优先
        depth = len(p.relative_to(run_dir).parts)
        return (pri, depth)

    candidates.sort(key=score)
    return candidates[0]


def read_run_config(run_dir: Path) -> Dict:
    cfg_path = run_dir / "run_config.yaml"
    if cfg_path.exists():
        try:
            return load_yaml(cfg_path)
        except Exception:
            return {}
    return {}


def _guess_rating_column(df: pd.DataFrame) -> str:
    """
    先按常见列名匹配；否则从数值列里猜一个“最像 1-100 评分”的列。
    """
    cols = list(df.columns)
    low_cols = {c.lower(): c for c in cols}

    for key in ["rating", "score", "response", "answer", "value"]:
        if key in low_cols:
            return low_cols[key]

    # 猜测：找数值列，且大部分落在 1..100
    numeric_cols = []
    for c in cols:
        if pd.api.types.is_numeric_dtype(df[c]):
            numeric_cols.append(c)

    if not numeric_cols:
        raise ValueError("未找到任何数值列，无法识别 rating 列。请检查 Exp2 CSV。")

    best_c = None
    best_score = -1.0
    for c in numeric_cols:
        x = df[c].to_numpy(dtype=float)
        x = x[np.isfinite(x)]
        if x.size < 5:
            continue
        in_range = np.mean((x >= 1) & (x <= 100))
        near_int = np.mean(np.isclose(x, np.round(x), atol=1e-6))
        s = 0.7 * in_range + 0.3 * near_int
        if s > best_score:
            best_score = s
            best_c = c

    if best_c is None:
        raise ValueError("无法自动识别 rating 列。请用 --rating_col 指定。")
    return best_c


def _guess_trial_order(df: pd.DataFrame) -> Optional[str]:
    """
    若存在 trial index 列则用于排序；否则保持 CSV 行顺序。
    """
    cols = list(df.columns)
    low_cols = {c.lower(): c for c in cols}
    for key in ["trial", "trial_index", "trial_idx", "t", "index", "idx", "order", "seq", "sequence"]:
        if key in low_cols:
            return low_cols[key]
    return None


def load_exp2_sequence(
    exp2_csv: Path,
    rating_col: Optional[str],
    rating_min: int,
    rating_max: int,
) -> pd.DataFrame:
    df = pd.read_csv(exp2_csv)

    if rating_col is None:
        rating_col = _guess_rating_column(df)

    # 排序
    order_col = _guess_trial_order(df)
    if order_col is not None:
        try:
            df = df.sort_values(order_col, kind="mergesort").reset_index(drop=True)
        except Exception:
            df = df.reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

    # 清理 rating
    df = df.copy()
    df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
    df = df[np.isfinite(df[rating_col])]
    df = df[(df[rating_col] >= rating_min) & (df[rating_col] <= rating_max)]
    df[rating_col] = df[rating_col].round().astype(int)

    df = df.reset_index(drop=True)
    df.attrs["rating_col"] = rating_col
    df.attrs["order_col"] = order_col or ""
    return df


# ----------------------------
# Stats
# ----------------------------
@dataclass
class NBackResult:
    n: int
    delta: float
    p_value: float
    mean_low: float
    mean_high: float
    n_low: int
    n_high: int


def welch_t_pvalue(x: np.ndarray, y: np.ndarray) -> float:
    if scipy_stats is None:
        raise RuntimeError("scipy 未安装，无法进行 Welch t-test。可将 test 改为 permutation。")
    res = scipy_stats.ttest_ind(x, y, equal_var=False, nan_policy="omit")
    return float(res.pvalue)


def permutation_pvalue(
    x: np.ndarray,
    y: np.ndarray,
    n_perm: int = 10000,
    seed: int = 123,
) -> float:
    """
    双侧置换检验：检验两组均值差异。
    """
    rng = np.random.default_rng(seed)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    if x.size < 2 or y.size < 2:
        return float("nan")

    obs = float(np.mean(y) - np.mean(x))  # 与 delta 定义一致：high - low（由外部保证传入顺序）
    pool = np.concatenate([x, y])
    n_x = x.size

    count = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        x_p = pool[:n_x]
        y_p = pool[n_x:]
        diff = float(np.mean(y_p) - np.mean(x_p))
        if abs(diff) >= abs(obs):
            count += 1
    return (count + 1) / (n_perm + 1)


def compute_n_back(
    ratings: pd.Series,
    n: int,
    low_max: int,
    high_min: int,
    test: str,
    n_perm: int,
    seed: int,
) -> NBackResult:
    """
    class 来源：rating_{t-n}，被分成 low/high；
    因变量：rating_t。
    pandas.shift(periods=n) 对齐规则：
      - n>0: shift(1) 是 1-back（上一试次）
      - n<0: shift(-1) 是 “未来 1”（control 用）
    """
    r = ratings.astype(float)

    anchor = r.shift(n)  # rating_{t-n} 对齐到 t 行
    cls = pd.Series(np.nan, index=r.index)

    cls[(anchor >= 1) & (anchor <= low_max)] = 0  # low
    cls[anchor >= high_min] = 1  # high

    # 仅保留有类别的行
    mask = np.isfinite(cls.to_numpy())
    r_t = r[mask].to_numpy(dtype=float)
    cls_v = cls[mask].to_numpy(dtype=float)

    low = r_t[cls_v == 0]
    high = r_t[cls_v == 1]

    mean_low = float(np.mean(low)) if low.size else float("nan")
    mean_high = float(np.mean(high)) if high.size else float("nan")
    delta = mean_high - mean_low

    if low.size < 2 or high.size < 2:
        p = float("nan")
    else:
        if test.lower() == "welch":
            # Welch: 比较两组的 rating_t 均值差异
            # 注意：Welch t-test 的 p 值与 (high-low) 的方向无关
            p = welch_t_pvalue(high, low)  # 顺序不影响 p，但保持一致
        elif test.lower() == "permutation":
            p = permutation_pvalue(low, high, n_perm=n_perm, seed=seed)
        else:
            raise ValueError(f"未知 test={test}，请用 welch 或 permutation")

    return NBackResult(
        n=int(n),
        delta=float(delta),
        p_value=float(p),
        mean_low=mean_low,
        mean_high=mean_high,
        n_low=int(low.size),
        n_high=int(high.size),
    )


# ----------------------------
# Plot
# ----------------------------
def format_run_params_for_plot(run_cfg: Dict) -> str:
    """
    尽量从 run_config.yaml 里提取常见字段；提取不到就留空。
    """
    def pick(*keys, default=""):
        for k in keys:
            if k in run_cfg:
                return run_cfg.get(k, default)
        return default

    model = pick("model", "model_name", "llm_model", default="")
    n_words = pick("n_words", "num_words", default="")
    dim = pick("dimension", "dim", default="")
    condition = pick("condition", default="Exp2")
    seed = pick("seed", default="")
    temperature = pick("temperature", default="")

    parts = []
    if model != "":
        parts.append(f"model: {model}")
    if n_words != "":
        parts.append(f"n_words: {n_words}")
    if dim != "":
        parts.append(f"dimension: {dim}")
    if condition != "":
        parts.append(f"condition: {condition}")
    if seed != "":
        parts.append(f"seed: {seed}")
    if temperature != "":
        parts.append(f"temperature: {temperature}")

    return "\n".join(parts)


def plot_delta_vs_n(
    results: List[NBackResult],
    out_png: Optional[Path],
    out_pdf: Optional[Path],
    dpi: int,
    run_params_text: str,
) -> None:
    ns = [r.n for r in results]
    deltas = [r.delta for r in results]
    ps = [r.p_value for r in results]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ns, deltas, marker="o")
    ax.axhline(0.0, linewidth=1)

    ax.set_xlabel("n (class from rating_{t-n})")
    ax.set_ylabel("delta = mean(rating_t | high) - mean(rating_t | low)")
    ax.set_title("prev-n-class effect: delta vs n")

    # 标注 p 值
    for n, d, p in zip(ns, deltas, ps):
        if np.isfinite(d) and np.isfinite(p):
            label = f"p={p:.3g}"
        else:
            label = "p=NA"
        ax.annotate(
            label,
            (n, d),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # run 参数文本（不显式指定颜色）
    if run_params_text.strip():
        ax.text(
            0.02,
            0.98,
            run_params_text,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9,
            bbox=dict(boxstyle="round", pad=0.3),
        )

    ax.set_xticks(ns)

    fig.tight_layout()
    if out_png is not None:
        fig.savefig(out_png, dpi=dpi)
    if out_pdf is not None:
        fig.savefig(out_pdf)
    plt.close(fig)


# ----------------------------
# Main
# ----------------------------
def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    default_params = here / "params.yaml"

    p = argparse.ArgumentParser(
        description="prev-n-class (low/high) n-back analysis for Exp2 sequence; output delta & p and delta-vs-n plot."
    )
    p.add_argument("--run_dir", type=str, required=True, help="run directory, e.g., outputs/<run_tag>")
    p.add_argument("--params", type=str, default=str(default_params), help="YAML params file path")
    p.add_argument("--k", type=int, default=None, help="single n value (overrides n_values in params)")
    p.add_argument("--exp2_csv", type=str, default=None, help="explicit Exp2 CSV path (optional)")
    p.add_argument("--rating_col", type=str, default=None, help="explicit rating column name (optional)")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.exists():
        raise FileNotFoundError(f"run_dir 不存在：{run_dir}")

    params_path = Path(args.params).resolve()
    if not params_path.exists():
        raise FileNotFoundError(f"params 文件不存在：{params_path}")

    params = load_yaml(params_path)

    # n values
    if args.k is not None:
        n_values = [int(args.k)]
    else:
        n_values = [int(x) for x in (params.get("n_values") or [])]
        if not n_values:
            raise ValueError("params.yaml 里没有 n_values，或者为空。")

    low_max = params.get("prevclass_bar", {}).get("prev_resp_low_max", 40)
    high_min = params.get("prevclass_bar", {}).get("prev_resp_high_min", 60)
    rating_min = int(params.get("rating_min", 1))
    rating_max = int(params.get("rating_max", 100))

    test = str(params.get("test", "welch"))
    n_perm = int(params.get("n_perm", 10000))
    seed = int(params.get("seed", 123))

    save_png = bool(params.get("save_png", True))
    save_pdf = bool(params.get("save_pdf", True))
    dpi = int(params.get("dpi", 200))

    # locate exp2 csv
    if args.exp2_csv is not None:
        exp2_csv = Path(args.exp2_csv).resolve()
        if not exp2_csv.exists():
            raise FileNotFoundError(f"--exp2_csv 不存在：{exp2_csv}")
    else:
        exp2_csv = find_exp2_csv(run_dir)

    # load data
    df = load_exp2_sequence(
        exp2_csv=exp2_csv,
        rating_col=args.rating_col,
        rating_min=rating_min,
        rating_max=rating_max,
    )
    rating_col = df.attrs["rating_col"]
    ratings = df[rating_col]

    # compute
    results: List[NBackResult] = []
    for n in n_values:
        res = compute_n_back(
            ratings=ratings,
            n=n,
            low_max=low_max,
            high_min=high_min,
            test=test,
            n_perm=n_perm,
            seed=seed,
        )
        results.append(res)

    # output dir
    out_root = Path(__file__).resolve().parent / "results"
    run_name = run_dir.name
    out_dir = out_root / run_name
    safe_mkdir(out_dir)

    # save stats
    stats_df = pd.DataFrame([r.__dict__ for r in results]).sort_values("n")
    stats_csv = out_dir / "n_back_stats.csv"
    stats_df.to_csv(stats_csv, index=False, encoding="utf-8")

    # save meta
    run_cfg = read_run_config(run_dir)
    meta = {
        "run_dir": str(run_dir),
        "run_name": run_name,
        "exp2_csv": str(exp2_csv),
        "rating_col": rating_col,
        "params_path": str(params_path),
        "params": params,
        "args": {
            "k": args.k,
            "rating_col": args.rating_col,
        },
        "run_config": run_cfg,
    }
    with (out_dir / "meta.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # plot
    run_params_text = format_run_params_for_plot(run_cfg)
    out_png = (out_dir / "delta_vs_n.png") if save_png else None
    out_pdf = (out_dir / "delta_vs_n.pdf") if save_pdf else None
    plot_delta_vs_n(
        results=sorted(results, key=lambda x: x.n),
        out_png=out_png,
        out_pdf=out_pdf,
        dpi=dpi,
        run_params_text=run_params_text,
    )

    # print a concise summary
    # (方便在终端查看；不影响文件输出)
    print(f"[OK] run={run_name}")
    print(f"  Exp2 CSV: {exp2_csv}")
    print(f"  rating_col: {rating_col}")
    print(f"  saved: {stats_csv}")
    if out_png:
        print(f"  saved: {out_png}")
    if out_pdf:
        print(f"  saved: {out_pdf}")


if __name__ == "__main__":
    main()
