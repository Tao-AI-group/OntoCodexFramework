
from typing import Tuple
import re

def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s\-\_\:]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s

def token_set_ratio(a: str, b: str) -> float:
    A, B = set(normalize(a).split()), set(normalize(b).split())
    if not A or not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    return inter / union

def levenshtein_ratio(a: str, b: str) -> float:
    a, b = normalize(a), normalize(b)
    if a == b:
        return 1.0
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return 0.0
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        curr = [i] + [0]*lb
        for j in range(1, lb + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            curr[j] = min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + cost)
        prev = curr
    dist = prev[lb]
    return 1.0 - dist / max(la, lb)

def combo_similarity(a: str, b: str) -> float:
    return 0.6 * token_set_ratio(a, b) + 0.4 * levenshtein_ratio(a, b)
