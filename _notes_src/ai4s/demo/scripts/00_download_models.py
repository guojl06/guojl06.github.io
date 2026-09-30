import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from huggingface_hub import snapshot_download

from src.config_utils import configure_hf_cache_env, load_config, resolve_cache_dir


def parse_args():
    p = argparse.ArgumentParser(description="Download/cache Hugging Face model files to a chosen local path.")
    p.add_argument("--config", default=None, help="Config JSON containing model_id and cache settings.")
    p.add_argument("--model-id", default=None, help="Hugging Face model id, e.g. EleutherAI/pythia-70m.")
    p.add_argument("--cache-dir", default=None, help="Optional local HF cache root. Example: /Volumes/Data/hf_cache or ./hf_cache")
    p.add_argument("--revision", default=None, help="Optional model revision/branch/commit.")
    p.add_argument("--local-dir", default=None, help="Optional plain local copy directory. Usually cache-dir is enough.")
    p.add_argument("--allow-patterns", nargs="*", default=None, help="Optional file patterns to include, e.g. *.json *.safetensors tokenizer.*")
    p.add_argument("--ignore-patterns", nargs="*", default=None, help="Optional file patterns to ignore.")
    p.add_argument("--token", default=None, help="Hugging Face token for gated models. You can also run `huggingface-cli login`.")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config) if args.config else {}
    model_id = args.model_id or cfg.get("model_id")
    if not model_id:
        raise SystemExit("Provide --model-id or --config with model_id.")

    cache_dir = resolve_cache_dir(cfg, args.cache_dir)
    configure_hf_cache_env(cache_dir)

    print("Model ID:", model_id)
    print("HF cache root:", cache_dir or "Hugging Face default")
    print("Local dir:", args.local_dir or "not used")

    path = snapshot_download(
        repo_id=model_id,
        repo_type="model",
        revision=args.revision,
        cache_dir=cache_dir,
        local_dir=args.local_dir,
        allow_patterns=args.allow_patterns,
        ignore_patterns=args.ignore_patterns,
        token=args.token,
    )
    print("Downloaded snapshot path:", path)

    manifest = {
        "model_id": model_id,
        "snapshot_path": path,
        "cache_dir": cache_dir,
        "local_dir": args.local_dir,
        "revision": args.revision,
    }
    out = Path("logs") / "download_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Manifest saved:", out)

if __name__ == "__main__":
    main()
