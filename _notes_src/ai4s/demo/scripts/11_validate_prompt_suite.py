import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config_utils import load_config
from src.model_utils import load_tokenizer
from src.prompt_utils import prompt_suite_from_config, read_jsonl, validate_prompt_rows


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/pythia_70m.json")
    p.add_argument("--prompt-suite", default=None)
    p.add_argument("--cache-dir", default=None)
    p.add_argument("--no-tokenizer", action="store_true", help="Only validate JSONL structure and unique IDs.")
    p.add_argument("--max-examples", type=int, default=None)
    p.add_argument("--strict", action="store_true", help="Exit nonzero if any validation error is found.")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)
    rows = prompt_suite_from_config(cfg, args.prompt_suite, args.max_examples)
    tokenizer = None if args.no_tokenizer else load_tokenizer(cfg, args.cache_dir)
    max_tokens = cfg.get("experiments", {}).get("global_defaults", {}).get("max_prompt_tokens")
    errors = validate_prompt_rows(rows, tokenizer=tokenizer, max_prompt_tokens=max_tokens)
    print(f"rows: {len(rows)}")
    print(f"errors: {len(errors)}")
    for e in errors[:50]:
        print(json.dumps({k:v for k,v in e.items() if k != 'row'}, ensure_ascii=False))
    if args.strict and errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
