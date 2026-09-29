"""Reproduce the semantic model's fixed holdout evaluation."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.model import evaluate

if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, ensure_ascii=False))
