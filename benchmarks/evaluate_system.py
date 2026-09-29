"""Evaluate the complete hybrid analyzer on a locked, non-training suite."""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.analyzer import analyze


if __name__ == "__main__":
    suite = json.loads((ROOT / "data" / "adversarial_suite.json").read_text(encoding="utf-8"))["cases"]
    matrix = {truth: {pred: 0 for pred in ("low", "medium", "high")} for truth in ("low", "medium", "high")}
    errors = []
    for case in suite:
        result = analyze(case["text"])
        predicted = result["level"]
        matrix[case["label"]][predicted] += 1
        if predicted != case["label"]:
            errors.append({"truth": case["label"], "predicted": predicted, "score": result["score"], "text": case["text"]})
    correct = sum(matrix[label][label] for label in matrix)
    report = {
        "suite_cases": len(suite),
        "class_balance": dict(Counter(case["label"] for case in suite)),
        "accuracy": round(correct / len(suite), 4),
        "confusion_matrix": matrix,
        "errors": errors,
        "disclosure": "This suite evaluates the complete rules-plus-model system and is not used for model training.",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
