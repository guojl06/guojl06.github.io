from typing import List, Dict, Any, Optional
from prompts import SYSTEM_PROMPT, build_user_prompt, build_none_prompt
from ci_utils import summary, ci95_half_width
import time
import re
import sys
import os
import json
from utils import append_jsonl, append_csv_dict


try:
    from tqdm import tqdm  # type: ignore
except Exception:
    class tqdm:
        def __init__(self, iterable=None, total=None, desc=None, leave=False, **kwargs):
            self.iterable = iterable
            self.total = total
            self._count = 0

        def __iter__(self):
            if self.iterable is None:
                return iter([])
            return iter(self.iterable)

        def update(self, n=1):
            self._count += n

        def set_postfix(self, *args, **kwargs):
            pass

        def close(self):
            pass


def _read_jsonl_rows(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not path or (not os.path.exists(path)):
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


class ExperimentRunner:
    def __init__(
        self,
        client,
        model: str,
        temperature: float,
        logs_dir: str,
        ci95_enable: bool,
        ci95_threshold: float,
        max_trials_per_word: int,
        rating_dimension: str = "concreteness",
        emotion_type: str = "joy",
    ):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.logs_dir = logs_dir
        self.ci95_enable = ci95_enable
        self.ci95_threshold = ci95_threshold
        self.max_trials_per_word = max_trials_per_word
        self.rating_dimension = rating_dimension
        self.emotion_type = emotion_type

    @staticmethod
    def _parse_rating_int_1_100(text: Optional[str]) -> Optional[int]:
        if not text:
            return None
        m = re.search(r"(?<!\d)(100|[1-9]\d?)(?!\d)", str(text))
        if not m:
            return None
        try:
            val = int(m.group(1))
        except ValueError:
            return None
        if 1 <= val <= 100:
            return val
        return None

    def _one_isolated_rating(self, word: str, dimension: Optional[str] = None) -> Dict[str, Any]:
        asked_dim = dimension or self.rating_dimension
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(word, asked_dim, emotion_type=self.emotion_type)},
        ]
        content = self.client.chat_completion(self.model, messages, self.temperature)
        rating = self._parse_rating_int_1_100(content)
        row = {
            "word": word,
            "response_text": content,
            "rating": rating,
            "asked_dimension": asked_dim,
        }
        if asked_dim == "emotion":
            row["asked_emotion_type"] = self.emotion_type
        return row

    @staticmethod
    def _validate_dimensions(words: List[str], dimensions: Optional[List[str]]) -> None:
        if dimensions is None:
            return
        if len(dimensions) != len(words):
            raise ValueError(
                f"dimensions length mismatch: len(words)={len(words)} but len(dimensions)={len(dimensions)}"
            )

    def run_experiment1_isolated(self, words: List[str], dimensions: Optional[List[str]] = None) -> Dict[str, Any]:
        self._validate_dimensions(words, dimensions)

        raw_rows: List[Dict[str, Any]] = []
        summary_rows: List[Dict[str, Any]] = []

        disable_bar = not sys.stderr.isatty()
        outer = tqdm(total=len(words), desc="Experiment 1 (isolated)", leave=True, disable=disable_bar)

        for i, w in enumerate(words):
            asked_dim = dimensions[i] if dimensions is not None else self.rating_dimension

            ratings: List[float] = []
            attempts = 0
            hw_display: Optional[float] = None

            while True:
                attempts += 1
                row = self._one_isolated_rating(w, asked_dim)
                raw_row = {
                    "word": w,
                    "rating": row["rating"],
                    "text": row["response_text"],
                    "asked_dimension": asked_dim,
                }
                if asked_dim == "emotion":
                    raw_row["asked_emotion_type"] = self.emotion_type
                raw_rows.append(raw_row)
                if row["rating"] is not None:
                    ratings.append(float(row["rating"]))

                if len(ratings) >= 2:
                    hw_display = ci95_half_width(ratings)
                    outer.set_postfix({"word": w, "dim": asked_dim, "n": len(ratings), "CI95": f"{hw_display:.3f}"})
                else:
                    outer.set_postfix({"word": w, "dim": asked_dim, "n": len(ratings)})

                if not self.ci95_enable:
                    break
                if len(ratings) >= 2:
                    hw = hw_display if hw_display is not None else ci95_half_width(ratings)
                    if hw <= self.ci95_threshold:
                        break
                if attempts >= self.max_trials_per_word:
                    break

            summ = summary(ratings) if ratings else {"mean": None, "std": None, "n": 0, "ci95_half_width": None}
            summary_row = {"word": w, "asked_dimension": asked_dim, **summ}
            if asked_dim == "emotion":
                summary_row["asked_emotion_type"] = self.emotion_type
            summary_rows.append(summary_row)
            outer.update(1)

        outer.close()
        return {"raw": raw_rows, "summary": summary_rows}

    def run_experiment2_sequential(
        self,
        words: List[str],
        dimensions: Optional[List[str]] = None,
        out_jsonl_path: Optional[str] = None,
        out_csv_path: Optional[str] = None,
        resume: bool = False,
        context_window: Optional[int] = None,
        compact_prompt: bool = False,
    ) -> Dict[str, Any]:
        self._validate_dimensions(words, dimensions)

        def _user_prompt(word: str, dim: str) -> str:
            if compact_prompt:
                if dim == "emotion":
                    return f"emotion:{self.emotion_type}: {word}"
                return f"{dim}: {word}"
            return build_user_prompt(word, dim, emotion_type=self.emotion_type)

        raw_rows: List[Dict[str, Any]] = []
        start_i = 0

        if resume and out_jsonl_path and os.path.exists(out_jsonl_path):
            raw_rows = _read_jsonl_rows(out_jsonl_path)
            start_i = len(raw_rows)
            if start_i > len(words):
                raw_rows = raw_rows[: len(words)]
                start_i = len(raw_rows)

        messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

        if start_i > 0:
            ctx_rows = raw_rows
            if context_window is not None:
                k0 = int(context_window)
                if k0 < 0:
                    raise ValueError("context_window must be >= 0 or None")
                ctx_rows = raw_rows[-k0:] if k0 > 0 else []

            for r in ctx_rows:
                w0 = str(r.get("word"))
                dim0 = str(r.get("asked_dimension") or self.rating_dimension)
                messages.append({"role": "user", "content": _user_prompt(w0, dim0)})
                messages.append({"role": "assistant", "content": str(r.get("text") or "")})

        disable_bar = not sys.stderr.isatty()
        try:
            bar = tqdm(total=len(words), desc="Experiment 2 (sequential)", leave=True, disable=disable_bar, initial=start_i)
        except TypeError:
            bar = tqdm(total=len(words), desc="Experiment 2 (sequential)", leave=True, disable=disable_bar)
            if start_i:
                bar.update(start_i)

        for i in range(start_i, len(words)):
            w = words[i]
            asked_dim = dimensions[i] if dimensions is not None else self.rating_dimension

            user = {"role": "user", "content": _user_prompt(w, asked_dim)}
            messages.append(user)

            if context_window is not None:
                k = int(context_window)
                if k < 0:
                    raise ValueError("context_window must be >= 0 or None")
                keep = 2 * k + 1
                if len(messages) > 1 + keep:
                    messages = [messages[0]] + messages[-keep:]

            content = self.client.chat_completion(self.model, messages, self.temperature)
            rating = self._parse_rating_int_1_100(content)

            row = {"word": w, "rating": rating, "text": content, "asked_dimension": asked_dim}
            if asked_dim == "emotion":
                row["asked_emotion_type"] = self.emotion_type
            raw_rows.append(row)

            if out_jsonl_path:
                append_jsonl(out_jsonl_path, row)
            if out_csv_path:
                fieldnames = ["word", "rating", "text", "asked_dimension"]
                if asked_dim == "emotion":
                    fieldnames.append("asked_emotion_type")
                append_csv_dict(out_csv_path, row, fieldnames)

            messages.append({"role": "assistant", "content": content})

            bar.set_postfix({"word": w, "dim": asked_dim})
            bar.update(1)
            time.sleep(0.05)

        bar.close()
        return {"raw": raw_rows}

    def run_none_autoregressive(self, n_trials: int) -> Dict[str, Any]:
        if n_trials < 1:
            raise ValueError("n_trials must be >= 1")

        raw_rows: List[Dict[str, Any]] = []
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        disable_bar = not sys.stderr.isatty()
        bar = tqdm(total=n_trials, desc="Experiment NONE (autoregressive)", leave=True, disable=disable_bar)

        prev_rating: Optional[int] = None
        for t in range(1, n_trials + 1):
            messages.append({"role": "user", "content": build_none_prompt(t)})

            content = self.client.chat_completion(self.model, messages, self.temperature)
            rating = self._parse_rating_int_1_100(content)

            raw_rows.append({"trial": t, "rating": rating, "prev_rating": prev_rating, "text": content})
            messages.append({"role": "assistant", "content": content})

            if rating is not None:
                prev_rating = rating

            bar.set_postfix({"trial": t, "rating": rating})
            bar.update(1)
            time.sleep(0.05)

        bar.close()
        return {"raw": raw_rows}
