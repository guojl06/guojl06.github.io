import math
from typing import List, Dict

def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")

def std(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    var = sum((x - m)**2 for x in xs) / (len(xs) - 1)
    return var ** 0.5

def ci95_half_width(xs: List[float]) -> float:
    """Return ±half-width of 95% CI assuming normal approx: 1.96 * s / sqrt(n)."""
    n = len(xs)
    if n == 0:
        return float("inf")
    s = std(xs)
    return 1.96 * s / math.sqrt(n)

def summary(xs: List[float]) -> Dict[str, float]:
    return {
        "mean": mean(xs),
        "std": std(xs),
        "n": len(xs),
        "ci95_half_width": ci95_half_width(xs),
    }
