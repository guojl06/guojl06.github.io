# prompts.py

from typing import Optional

SYSTEM_PROMPT = (
    "You are a participant in a behavioral experiment. "
    "Reply with exactly one integer between 1 and 100 inclusive. "
    "Digits only: no words, no decimals, and no punctuation."
)

VALID_EMOTION_TYPES = (
    "anger",
    "anticipation",
    "disgust",
    "fear",
    "joy",
    "sadness",
    "surprise",
    "trust",
)


def normalize_emotion_type(emotion_type: Optional[str]) -> str:
    emo = str(emotion_type or "joy").strip().lower()
    if emo not in VALID_EMOTION_TYPES:
        raise ValueError(
            f"Unsupported emotion_type={emotion_type!r}. "
            f"Valid options: {', '.join(VALID_EMOTION_TYPES)}"
        )
    return emo


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
    emotion_type: Optional[str] = None,
) -> str:
    """
    根据 dimension 构造不同的评分指令:
      - 'concreteness'
      - 'valence'
      - 'arousal'
      - 'emotion'  (requires emotion_type, default joy)
      - 'none'     # number-only control condition (handled by build_none_prompt)
    """
    dim = str(dimension).strip().lower()

    if dim == "valence":
        instruction = (
            "Rate how the following single word makes a person feel on a 1-100 scale, "
            "where 1 means very negative, bad and 100 means very positive, good.\n"
        )
    elif dim == "arousal":
        instruction = (
            "Rate how the following single word makes a person feel on a 1-100 scale, "
            "where 1 means very calm, relaxed and 100 means very aroused, energized.\n"
        )
    elif dim == "emotion":
        emo = normalize_emotion_type(emotion_type)
        instruction = (
            f"Words can be associated with different degrees of {emo}. "
            f"Your task is to make the single-word version of a MOST/LEAST judgment.\n"
            f"Rate how strongly the following single word is associated with {emo} on a 1-100 scale, "
            f"where 1 means associated with the LEAST {emo} and 100 means associated with the MOST {emo}.\n"
            f"If the word has multiple meanings, judge it by the meaning most strongly associated with {emo}.\n"
        )
    else:
        instruction = (
            "Rate the concreteness of the following single word on a 1-100 scale, "
            "where 1 means very abstract and 100 means very concrete.\n"
        )

    return (
        instruction
        + f"The word is: {word}\n"
        + "Output: only answer a single integer from 1 to 100. "
          "No extra text, no decimals, no punctuation."
    )
