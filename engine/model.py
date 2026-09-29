"""Small, auditable semantic classifier trained locally from the bundled corpus.

The model uses multinomial Naive Bayes over word and character n-grams. It is
purposefully compact, deterministic, dependency-free at inference, and suited
to privacy-sensitive edge use. The corpus and evaluation split ship with the
repository so every metric can be reproduced.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "scam_corpus.json"
LABELS = ("low", "medium", "high")


def _features(text: str) -> Counter[str]:
    clean = re.sub(r"\s+", " ", text.casefold()).strip()
    words = re.findall(r"[\w@₹]+", clean, flags=re.UNICODE)
    feats: Counter[str] = Counter()
    for word in words:
        feats[f"w:{word}"] += 1
        padded = f"^{word}$"
        for n in (3, 4):
            for i in range(max(0, len(padded) - n + 1)):
                feats[f"c:{padded[i:i+n]}"] += 0.35
    for a, b in zip(words, words[1:]):
        feats[f"b:{a}_{b}"] += 0.8
    return feats


class SemanticModel:
    def __init__(self, records: list[dict]) -> None:
        by_label: dict[str, list[Counter[str]]] = defaultdict(list)
        vocab: set[str] = set()
        for record in records:
            f = _features(record["text"])
            by_label[record["label"]].append(f)
            vocab.update(f)
        self.vocab_size = len(vocab)
        self.log_prior: dict[str, float] = {}
        self.counts: dict[str, Counter[str]] = {}
        self.totals: dict[str, float] = {}
        total_docs = len(records)
        for label in LABELS:
            docs = by_label[label]
            self.log_prior[label] = math.log((len(docs) + 1) / (total_docs + len(LABELS)))
            merged: Counter[str] = Counter()
            for doc in docs:
                merged.update(doc)
            self.counts[label] = merged
            self.totals[label] = sum(merged.values())

    def predict(self, text: str) -> dict:
        feats = _features(text)
        scores = {}
        alpha = 0.75
        for label in LABELS:
            denom = self.totals[label] + alpha * self.vocab_size
            score = self.log_prior[label]
            for feature, value in feats.items():
                score += value * math.log((self.counts[label].get(feature, 0) + alpha) / denom)
            scores[label] = score
        maximum = max(scores.values())
        exp = {label: math.exp(score - maximum) for label, score in scores.items()}
        normalizer = sum(exp.values())
        probs = {label: exp[label] / normalizer for label in LABELS}
        label = max(probs, key=probs.get)
        return {"label": label, "confidence": round(probs[label], 4), "probabilities": {k: round(v, 4) for k, v in probs.items()}}


@lru_cache(maxsize=1)
def get_model() -> SemanticModel:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    return SemanticModel(corpus["train"])


def evaluate() -> dict:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    model = SemanticModel(corpus["train"])
    matrix = {truth: {pred: 0 for pred in LABELS} for truth in LABELS}
    errors = []
    for item in corpus["test"]:
        result = model.predict(item["text"])
        matrix[item["label"]][result["label"]] += 1
        if result["label"] != item["label"]:
            errors.append({"truth": item["label"], "predicted": result["label"], "confidence": result["confidence"], "text": item["text"]})
    total = len(corpus["test"])
    correct = sum(matrix[label][label] for label in LABELS)
    return {"train_samples": len(corpus["train"]), "test_samples": total, "accuracy": round(correct / total, 4), "confusion_matrix": matrix, "errors": errors}
