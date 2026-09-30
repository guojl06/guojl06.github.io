# prompts.py
import json

# 固定 key：每个 trial 只更新这个 key 的 value
STIMULUS_KEY = "stimulus_word"

SYSTEM_PROMPT = (
    "You are a participant in a behavioral experiment.\n"
    "Reply with exactly one integer between 1 and 100 inclusive.\n"
    "Digits only: no words, no decimals, and no punctuation.\n"
    "\n"
    "Important:\n"
    "- The user message may provide the stimulus as a key-value object.\n"
    "- Only the VALUE (the word) should be rated; the KEY name is not part of the stimulus.\n"
)


def _kv_obj(word: str, key: str = STIMULUS_KEY) -> str:
    """Render the stimulus as a stable key-value object (JSON)."""
    return json.dumps({key: str(word)}, ensure_ascii=False)


def build_none_prompt(trial_index: int) -> str:
    """User prompt for the number-only (dimension='none') control condition."""
    return (
        f"Trial {trial_index}. Ignore any word meaning or features.\n"
        "Choose an integer from 1 to 100 (inclusive) as if sampling at random.\n"
        "Each choice should be independent of previous choices. Repeats are allowed.\n"
        "Do not follow patterns, do not try to balance frequencies, and do not avoid repeating numbers.\n"
        "Output: only one integer (1-100). Digits only."
    )


def build_user_prompt(
    word: str,
    dimension: str = "concreteness",
    *,
    compact: bool = False,
    stimulus_key: str = STIMULUS_KEY,
) -> str:
    """
    Build a rating prompt where the stimulus word is provided via a fixed key whose value updates each trial.

    dimension:
      - 'concreteness'
      - 'valence'
      - 'arousal'
      - 'none'  # handled by build_none_prompt
    compact:
      - True: minimal prompt body (useful for Exp2 compact mode)
      - False: full instruction (default)
    """
    # Construct instruction
    if dimension == "valence":
        instruction = (
            "Rate how the stimulus word makes a person feel on a 1-100 scale, "
            "where 1 means very negative (bad) and 100 means very positive (good)."
        )
    elif dimension == "arousal":
        instruction = (
            "Rate how the stimulus word makes a person feel on a 1-100 scale, "
            "where 1 means very calm/relaxed and 100 means very aroused/energized."
        )
    else:
        instruction = (
            "Rate the concreteness of the stimulus word on a 1-100 scale, "
            "where 1 means very abstract and 100 means very concrete."
        )

    stim = _kv_obj(word, key=stimulus_key)

    if compact:
        # 关键：格式恒定，只更新 stimulus_key 的 value
        return (
            f"{instruction}\n"
            f"Stimulus (key-value object): {stim}\n"
            "Output: one integer 1-100. Digits only."
        )

    return (
        f"{instruction}\n"
        "The stimulus word is provided as a key-value object below. "
        "Read ONLY the value under the fixed key and rate that word.\n"
        f"Stimulus (key-value object): {stim}\n"
        "Output: only answer a single integer from 1 to 100. "
        "No extra text, no decimals, no punctuation."
    )
