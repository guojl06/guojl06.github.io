from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .config_utils import project_path


def read_jsonl(path: str | Path) -> List[Dict[str, Any]]:
    path = project_path(path)
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {e}") from e
            obj["__source_file__"] = str(path)
            obj["__line_no__"] = line_no
            rows.append(obj)
    return rows


def filter_prompts(rows: List[Dict[str, Any]], tasks=None, conditions=None, tags=None, max_examples=None) -> List[Dict[str, Any]]:
    tasks = set(tasks or [])
    conditions = set(conditions or [])
    tags = set(tags or [])
    out = []
    for r in rows:
        if tasks and r.get("task") not in tasks:
            continue
        if conditions and r.get("condition") not in conditions:
            continue
        if tags and not tags.intersection(set(r.get("tags") or [])):
            continue
        out.append(r)
        if max_examples is not None and len(out) >= int(max_examples):
            break
    return out


def prompt_suite_from_config(cfg: Dict[str, Any], override_path: Optional[str] = None, max_examples: Optional[int] = None) -> List[Dict[str, Any]]:
    ps = cfg.get("prompt_suite", {})
    path = override_path or ps.get("path")
    if not path:
        raise ValueError("No prompt suite path provided. Use --prompt-suite or config['prompt_suite']['path'].")
    rows = read_jsonl(path)
    filt = ps.get("filter", {})
    return filter_prompts(
        rows,
        tasks=filt.get("tasks") or [],
        conditions=filt.get("conditions") or [],
        tags=filt.get("tags") or [],
        max_examples=max_examples if max_examples is not None else ps.get("max_examples"),
    )


def validate_prompt_rows(rows: List[Dict[str, Any]], tokenizer=None, max_prompt_tokens: Optional[int] = None, require_unique_ids: bool = True) -> List[Dict[str, Any]]:
    errors = []
    seen = set()
    for r in rows:
        pid = r.get("prompt_id")
        if not pid:
            errors.append({"prompt_id": pid, "error": "missing prompt_id", "row": r})
        elif require_unique_ids and pid in seen:
            errors.append({"prompt_id": pid, "error": "duplicate prompt_id", "row": r})
        seen.add(pid)

        task = r.get("task")
        target = r.get("target_text")
        if not target:
            errors.append({"prompt_id": pid, "error": "missing target_text", "row": r})
        elif tokenizer is not None:
            tids = tokenizer.encode(target, add_special_tokens=False)
            if len(tids) != 1:
                errors.append({"prompt_id": pid, "error": f"target_text is not single token: {target!r} -> {tids}", "row": r})

        if task == "activation_patching" or r.get("clean_prompt") or r.get("corrupt_prompt"):
            cp, kp = r.get("clean_prompt"), r.get("corrupt_prompt")
            if not cp or not kp:
                errors.append({"prompt_id": pid, "error": "activation patching item needs clean_prompt and corrupt_prompt", "row": r})
            elif tokenizer is not None:
                cids = tokenizer(cp, add_special_tokens=True)["input_ids"]
                kids = tokenizer(kp, add_special_tokens=True)["input_ids"]
                if len(cids) != len(kids):
                    errors.append({"prompt_id": pid, "error": f"clean/corrupt token lengths differ: {len(cids)} vs {len(kids)}", "row": r})
        else:
            prompt = r.get("prompt")
            if not prompt:
                errors.append({"prompt_id": pid, "error": "missing prompt", "row": r})
            elif tokenizer is not None and max_prompt_tokens is not None:
                n = len(tokenizer(prompt, add_special_tokens=True)["input_ids"])
                if n > max_prompt_tokens:
                    errors.append({"prompt_id": pid, "error": f"prompt too long: {n} > {max_prompt_tokens}", "row": r})
    return errors


def row_variables_json(row: Dict[str, Any]) -> str:
    return json.dumps(row.get("variables", {}), ensure_ascii=False, sort_keys=True)


def row_tags_json(row: Dict[str, Any]) -> str:
    return json.dumps(row.get("tags", []), ensure_ascii=False)
