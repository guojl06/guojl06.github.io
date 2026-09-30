from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def project_path(path_like: str | Path) -> Path:
    p = Path(path_like)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p


def load_config(path: str | Path) -> Dict[str, Any]:
    path = project_path(path)
    with path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["__config_path__"] = str(path)
    return cfg


def get_nested(cfg: Dict[str, Any], keys: list[str], default: Any = None) -> Any:
    cur: Any = cfg
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def resolve_cache_dir(cfg: Dict[str, Any], override: Optional[str] = None) -> Optional[str]:
    """Resolve Hugging Face cache directory.

    Priority:
      1. explicit CLI override
      2. top-level config['cache_dir'] if not auto/null
      3. config['runtime']['cache_dir'] if not auto/null
      4. env HF_HUB_CACHE
      5. env HF_HOME
      6. None -> Hugging Face default
    """
    candidates = [
        override,
        cfg.get("cache_dir"),
        get_nested(cfg, ["runtime", "cache_dir"]),
        os.environ.get("HF_HUB_CACHE"),
        os.environ.get("HF_HOME"),
    ]
    for c in candidates:
        if c and str(c).lower() not in {"auto", "none", "null"}:
            return str(project_path(c) if not Path(str(c)).is_absolute() else Path(str(c)))
    return None


def configure_hf_cache_env(cache_dir: Optional[str] = None) -> None:
    """Set HF_HOME and HF_HUB_CACHE for the current process.

    If cache_dir is /path/hf_cache, HF_HOME=/path/hf_cache and
    HF_HUB_CACHE=/path/hf_cache/hub unless cache_dir already ends with hub.
    """
    if not cache_dir:
        return
    cache_path = Path(cache_dir).expanduser().resolve()
    if cache_path.name == "hub":
        hf_home = cache_path.parent
        hf_hub_cache = cache_path
    else:
        hf_home = cache_path
        hf_hub_cache = cache_path / "hub"
    hf_home.mkdir(parents=True, exist_ok=True)
    hf_hub_cache.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(hf_home)
    os.environ["HF_HUB_CACHE"] = str(hf_hub_cache)


def output_paths(cfg: Dict[str, Any]) -> Dict[str, Path]:
    out = cfg.get("outputs", {})
    return {
        "root": project_path(out.get("root", "outputs")),
        "results": project_path(out.get("results_dir", "outputs/results")),
        "activations": project_path(out.get("activations_dir", "outputs/activations")),
        "figures": project_path(out.get("figures_dir", "outputs/figures")),
    }


def file_prefix(cfg: Dict[str, Any]) -> str:
    return cfg.get("outputs", {}).get("file_prefix") or cfg.get("name") or cfg.get("model_id", "model").replace("/", "_")
