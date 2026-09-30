#!/usr/bin/env bash
set -euo pipefail

for i in {1..3}; do
  echo "===== Run $i / 3 ====="

  python src/main.py \
    --which exp2 \
    --n_words 1000 \
    --model "gpt-4o" \
    --temperature 1.0 \
    --ci95_enable \
    --ci95_threshold 1 \
    --valence \
    --exp2_context_window 30 \
    --excel_path testing_data/Warriner_et_alemotratings.csv

  python ana_norms_bias_sd/analyze_norms_bias_sd.py
done
