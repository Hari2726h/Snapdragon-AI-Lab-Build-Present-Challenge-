# Judging evidence map

## Technical implementation

- Working local HTTP product with single-message and conversation APIs
- Trained semantic classifier with visible probabilities and a fixed holdout
- Explainable rules for URLs, credentials, payments, pressure, and impersonation
- Conversation progression engine with per-turn scores and attack-chain stages
- Ten deterministic regression tests
- Locked 45-case end-to-end evaluation with every error printed
- QNN adapter, INT8 model contract, CPU fallback, and Snapdragon acceptance checks

## Application use case and innovation

Most safety tools inspect one URL or one message. Rakshak Edge detects the social-engineering sequence across a conversation: identity setup, isolation, then extraction. This supports linkless scams such as executive impersonation, digital arrest, family emergency, and task fraud.

## Deployment and accessibility

- One-command demo with no package installation
- Loopback-only API, no telemetry, no account, and no raw history
- Keyboard navigation, high contrast, reduced motion, and plain-language actions
- Privacy-safe report export that excludes the source message
- Production profile for ONNX Runtime QNN on Snapdragon X Series

## Presentation and documentation

- Live 90-second demo script
- Architecture, threat model, and Snapdragon deployment guide
- Reproducible evaluation commands in the README
- Submission brief plus editable PPTX and PDF deck

## Reproduction

```bash
python -m unittest discover -s tests -v
python benchmarks/evaluate_model.py
python benchmarks/evaluate_system.py
python benchmarks/run_benchmark.py
python app.py
```
