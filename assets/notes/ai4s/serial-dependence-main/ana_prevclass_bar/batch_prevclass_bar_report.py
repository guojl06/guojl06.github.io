"""Batch prev-class analysis + report generation.

Repo assumptions
----------------
- Run outputs live under: <project_root>/outputs/<run_tag>/
- Each run contains: run_config.yaml (for metadata)
- Prev-class analysis outputs live under:
    <project_root>/ana_prevclass_bar/results/<run_tag>/
      - prevclass_bar.png
      - prevclass_summary.json
- The analyzer is: <project_root>/ana_prevclass_bar/analyze_prevclass_bar.py

What this script does
---------------------
1) Scan outputs/* run folders.
2) Select eligible runs:
   - single-dimension: dimension in {concreteness, valence, arousal}
   - mixed: dimension == 'mixed'
   - skip: '2d', 'none', and anything else
   - require Exp2 data (exp2_sequential_raw.csv OR combined_overview.csv)
3) For each eligible run, if analysis outputs are missing, run:
     python src/analyze_prevclass_bar.py --run-dir outputs/<run_tag> --n-perm <N>
4) Generate a Word report (docx) under:
     ana_prevclass_bar/prevclass_bar_report.docx
   with two sections: single-dimension runs and mixed-dimension runs.

Notes
-----
- Compatible with both old and new run folder naming (whether 'model' appears
  in the folder name or not). Metadata is read primarily from run_config.yaml
  and falls back to parsing the folder name when needed.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import yaml


VALID_SINGLE_DIMS = ("concreteness", "valence", "arousal")
SKIP_DIMS = ("none", "2d")


def project_root_dir() -> str:
    """Best-effort project root detection."""
    here = os.path.abspath(os.path.dirname(__file__))  # .../ana_prevclass_bar
    parent = os.path.abspath(os.path.join(here, ".."))
    if os.path.isdir(os.path.join(parent, "outputs")) or os.path.exists(os.path.join(parent, "config.yaml")):
        return parent
    if os.path.isdir(os.path.join(here, "outputs")) or os.path.exists(os.path.join(here, "config.yaml")):
        return here
    return parent


def safe_load_yaml(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            obj = yaml.safe_load(f) or {}
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    return {}


def parse_n_from_run_tag(run_tag: str) -> Optional[int]:
    m = re.search(r"(?:^|_)n(\d+)(?:_|$)", run_tag)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def infer_model_from_run_tag(run_tag: str) -> Optional[str]:
    """Infer model from run_tag if possible.

    New naming example:
      20251224_101010_gpt-4o-mini_both_concreteness_n400
    Old naming example (no model):
      20251213_133659_both_concreteness_n400

    Heuristic: split by '_' and look at the 3rd token.
    - If token[2] is 'exp1/exp2/both', then model is missing.
    - Else token[2] is treated as the model.
    """
    parts = run_tag.split("_")
    if len(parts) < 4:
        return None
    third = parts[2]
    if third in ("exp1", "exp2", "both"):
        return None
    return third


def infer_which_from_run_tag(run_tag: str) -> Optional[str]:
    parts = run_tag.split("_")
    if len(parts) < 4:
        return None
    third = parts[2]
    if third in ("exp1", "exp2", "both"):
        return third
    fourth = parts[3]
    if fourth in ("exp1", "exp2", "both"):
        return fourth
    return None


@dataclass
class RunMeta:
    run_tag: str
    run_dir: str
    model: str
    which: str
    dimension: str
    n_words: Optional[int]
    temperature: Optional[float] = None
    mixed_dims: Optional[Tuple[str, str]] = None


def extract_run_meta(run_dir: str) -> Optional[RunMeta]:
    run_tag = os.path.basename(os.path.normpath(run_dir))
    cfg_path = os.path.join(run_dir, "run_config.yaml")
    cfg = safe_load_yaml(cfg_path) if os.path.exists(cfg_path) else {}

    merged = cfg.get("merged_cfg") if isinstance(cfg.get("merged_cfg"), dict) else {}

    def _pick(key: str, default: Any = None) -> Any:
        v = cfg.get(key, None)
        if v is None and isinstance(merged, dict):
            v = merged.get(key, None)
        return default if v is None else v

    dimension = str(_pick("dimension", "")).strip().lower() or "unknown"
    if dimension in SKIP_DIMS:
        return None

    which = str(_pick("which", "")).strip().lower()
    if not which:
        which = infer_which_from_run_tag(run_tag) or "unknown"

    model = str(_pick("model", "")).strip()
    if not model:
        model = infer_model_from_run_tag(run_tag) or "(unknown)"

    n_words = None
    if _pick("n_words", None) is not None:
        try:
            n_words = int(_pick("n_words"))
        except Exception:
            n_words = None
    if n_words is None:
        n_words = parse_n_from_run_tag(run_tag)

    temperature = None
    if _pick("temperature", None) is not None:
        try:
            temperature = float(_pick("temperature"))
        except Exception:
            temperature = None

    mixed_dims = None
    if dimension == "mixed":
        md = _pick("mixed_dimensions", None)
        if isinstance(md, (list, tuple)) and len(md) == 2:
            mixed_dims = (str(md[0]), str(md[1]))
        else:
            md2 = _pick("mixed_dims", None) or _pick("mixed", None)
            if isinstance(md2, (list, tuple)) and len(md2) == 2:
                mixed_dims = (str(md2[0]), str(md2[1]))

        if mixed_dims is None:
            m = re.search(r"mixed_([a-zA-Z]+)_([a-zA-Z]+)", run_tag)
            if m:
                mixed_dims = (m.group(1), m.group(2))

    return RunMeta(
        run_tag=run_tag,
        run_dir=run_dir,
        model=model,
        which=which,
        dimension=dimension,
        n_words=n_words,
        temperature=temperature,
        mixed_dims=mixed_dims,
    )


def has_exp2_data(run_dir: str) -> bool:
    return os.path.exists(os.path.join(run_dir, "exp2_sequential_raw.csv")) or os.path.exists(
        os.path.join(run_dir, "combined_overview.csv")
    )


def analysis_paths(root: str, run_tag: str) -> Tuple[str, str]:
    out_dir = os.path.join(root, "ana_prevclass_bar", "results", run_tag)
    fig_path = os.path.join(out_dir, "prevclass_bar.png")
    summary_path = os.path.join(out_dir, "prevclass_summary.json")
    return fig_path, summary_path


def ensure_prevclass_analysis(root: str, run_meta: RunMeta, n_perm: int, perm_seed: int) -> Tuple[bool, Optional[str]]:
    """Ensure analysis exists. Returns (ok, error_message)."""
    fig_path, summary_path = analysis_paths(root, run_meta.run_tag)
    if os.path.exists(fig_path) and os.path.exists(summary_path):
        if int(n_perm) > 0:
            try:
                with open(summary_path, "r", encoding="utf-8") as f:
                    s = json.load(f)
                pt = s.get("permutation_test")
                if isinstance(pt, dict):
                    prev_n = int(pt.get("n_perm") or 0)
                    if prev_n >= int(n_perm):
                        return True, None
            except Exception:
                pass
        else:
            return True, None

    analyzer = os.path.join(root, "ana_prevclass_bar", "analyze_prevclass_bar.py")
    if not os.path.exists(analyzer):
        return False, f"Analyzer not found: {analyzer}"

    cmd = [
        sys.executable,
        analyzer,
        "--run-dir",
        run_meta.run_dir,
        "--n-perm",
        str(int(n_perm)),
        "--perm-seed",
        str(int(perm_seed)),
    ]

    try:
        subprocess.run(cmd, cwd=root, check=True)
    except subprocess.CalledProcessError as e:
        return False, f"analyze_prevclass_bar failed (run={run_meta.run_tag}): {e}"

    if os.path.exists(fig_path) and os.path.exists(summary_path):
        return True, None
    return False, f"Analysis did not produce expected outputs for run={run_meta.run_tag}"


@dataclass
class AnalysisRecord:
    meta: RunMeta
    fig_path: Optional[str]
    perm_p: Optional[float]
    welch_p: Optional[float]
    delta: Optional[float]
    note: Optional[str] = None


def load_analysis_record(root: str, meta: RunMeta) -> AnalysisRecord:
    fig_path, summary_path = analysis_paths(root, meta.run_tag)

    perm_p = None
    welch_p = None
    delta = None
    note = None

    if os.path.exists(summary_path):
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                s = json.load(f)
            delta = float(s.get("delta_high_minus_low")) if s.get("delta_high_minus_low") is not None else None
            wt = s.get("welch_ttest")
            if isinstance(wt, dict) and wt.get("p_value") is not None:
                welch_p = float(wt.get("p_value"))
            pt = s.get("permutation_test")
            if isinstance(pt, dict) and pt.get("p_value") is not None:
                perm_p = float(pt.get("p_value"))
        except Exception as e:
            note = f"Failed to parse summary JSON: {e}"

    fig_path2 = fig_path if os.path.exists(fig_path) else None
    return AnalysisRecord(meta=meta, fig_path=fig_path2, perm_p=perm_p, welch_p=welch_p, delta=delta, note=note)


def build_docx_report(records_single: List[AnalysisRecord], records_mixed: List[AnalysisRecord], out_path: str) -> None:
    try:
        from docx import Document  # type: ignore
        from docx.shared import Inches  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "python-docx is required to generate a Word report. "
            "Install it via: pip install python-docx\n"
            f"Import error: {e}"
        )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    doc = Document()

    doc.add_heading("Prev-class (low/high) analysis report", level=0)
    doc.add_paragraph(f"Generated at: {_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def _add_section(title: str, records: List[AnalysisRecord]) -> None:
        doc.add_heading(title, level=1)
        if not records:
            doc.add_paragraph("(No eligible runs found.)")
            return

        for rec in records:
            meta = rec.meta
            doc.add_heading(meta.run_tag, level=2)

            tbl = doc.add_table(rows=1, cols=2)
            left = tbl.cell(0, 0)
            right = tbl.cell(0, 1)

            if rec.fig_path and os.path.exists(rec.fig_path):
                p = left.paragraphs[0]
                run = p.add_run()
                run.add_picture(rec.fig_path, width=Inches(4.7))
            else:
                left.text = "(missing prevclass_bar.png)"

            lines: List[str] = []
            lines.append(f"model: {meta.model}")
            lines.append(f"which: {meta.which}")
            lines.append(f"dimension: {meta.dimension}")
            if meta.temperature is not None:
                lines.append(f"temperature: {meta.temperature}")
            if meta.dimension == "mixed":
                if meta.mixed_dims is not None:
                    lines.append(f"mixed dims: {meta.mixed_dims[0]} / {meta.mixed_dims[1]}")
                else:
                    lines.append("mixed dims: (unknown)")
            if meta.n_words is not None:
                lines.append(f"n_words: {meta.n_words}")

            if rec.delta is not None:
                lines.append(f"delta (high-low): {rec.delta:.6f}")

            if rec.perm_p is not None:
                lines.append(f"p_value (permutation): {rec.perm_p:.6g}")
            if rec.welch_p is not None:
                lines.append(f"p_value (Welch t-test): {rec.welch_p:.6g}")

            if rec.note:
                lines.append(f"note: {rec.note}")

            right.text = "\n".join(lines)
            doc.add_paragraph("")

    _add_section("Single-dimension runs", records_single)
    _add_section("Mixed-dimension runs", records_mixed)

    doc.save(out_path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Scan outputs, run prevclass analysis, and generate a Word report.")
    ap.add_argument("--outputs-dir", type=str, default="outputs", help="Outputs directory under project root.")
    ap.add_argument(
        "--report-dir",
        type=str,
        default="ana_prevclass_bar",
        help="Directory (under project root) to write the final report file.",
    )
    ap.add_argument("--n-perm", type=int, default=10000, help="Permutation shuffles to pass to analyze_prevclass_bar.py")
    ap.add_argument("--perm-seed", type=int, default=0)
    ap.add_argument(
        "--report-name",
        type=str,
        default="prevclass_bar_report.docx",
        help="Report filename to write under ana_prevclass_bar/.",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Only scan and print what would be done; do not run analyses or write the report.",
    )
    args = ap.parse_args()

    root = project_root_dir()
    outputs_dir = os.path.join(root, args.outputs_dir)
    if not os.path.isdir(outputs_dir):
        raise FileNotFoundError(f"Outputs directory not found: {outputs_dir}")

    run_metas: List[RunMeta] = []
    for name in sorted(os.listdir(outputs_dir)):
        run_dir = os.path.join(outputs_dir, name)
        if not os.path.isdir(run_dir):
            continue
        cfg_path = os.path.join(run_dir, "run_config.yaml")
        if not os.path.exists(cfg_path):
            continue
        meta = extract_run_meta(run_dir)
        if meta is None:
            continue
        if meta.dimension not in VALID_SINGLE_DIMS and meta.dimension != "mixed":
            continue
        if not has_exp2_data(run_dir):
            continue
        run_metas.append(meta)

    if not run_metas:
        print("[WARN] No eligible runs found under outputs/.")

    failures: List[str] = []
    ensured: List[RunMeta] = []

    for meta in run_metas:
        fig_path, summary_path = analysis_paths(root, meta.run_tag)
        already = os.path.exists(fig_path) and os.path.exists(summary_path)

        if args.dry_run:
            if already:
                print(f"[SKIP] already analyzed: {meta.run_tag}")
            else:
                print(f"[TODO] analyze: {meta.run_tag}")
            ensured.append(meta)
            continue

        if already:
            ensured.append(meta)
            continue

        ok, err = ensure_prevclass_analysis(root, meta, n_perm=args.n_perm, perm_seed=args.perm_seed)
        if ok:
            ensured.append(meta)
        else:
            failures.append(err or f"unknown failure for run={meta.run_tag}")

    rec_single: List[AnalysisRecord] = []
    rec_mixed: List[AnalysisRecord] = []
    for meta in ensured:
        rec = load_analysis_record(root, meta)
        if meta.dimension == "mixed":
            rec_mixed.append(rec)
        else:
            rec_single.append(rec)

    rec_single.sort(key=lambda r: r.meta.run_tag)
    rec_mixed.sort(key=lambda r: r.meta.run_tag)

    report_path = os.path.join(root, args.report_dir, args.report_name)
    if args.dry_run:
        print(f"[DRY] would write report: {report_path}")
    else:
        build_docx_report(rec_single, rec_mixed, out_path=report_path)
        print(f"[OK] Wrote report: {report_path}")

    if failures:
        print("\n[WARN] Some runs failed analysis:")
        for s in failures:
            print(" -", s)


if __name__ == "__main__":
    main()
