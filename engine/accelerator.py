"""Optional Snapdragon QNN adapter.

The deterministic engine remains authoritative when no model is installed. This
adapter provides the production path for a fine-tuned INT8 classifier.
"""

from __future__ import annotations

import os
from pathlib import Path


class Accelerator:
    def __init__(self, model_path: str = "models/scam_classifier.onnx") -> None:
        self.model_path = Path(model_path)
        self.requested = os.getenv("RAKSHAK_BACKEND", "auto").lower()
        self.session = None
        self.provider = "deterministic"

    def load(self) -> str:
        if not self.model_path.exists():
            return self.provider
        try:
            import onnxruntime as ort  # type: ignore

            available = ort.get_available_providers()
            providers = ["QNNExecutionProvider", "CPUExecutionProvider"] if "QNNExecutionProvider" in available else ["CPUExecutionProvider"]
            if self.requested == "cpu":
                providers = ["CPUExecutionProvider"]
            self.session = ort.InferenceSession(str(self.model_path), providers=providers)
            self.provider = self.session.get_providers()[0]
        except (ImportError, OSError, RuntimeError):
            self.session = None
        return self.provider
