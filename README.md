# Rakshak Edge

**A private, on-device social-engineering firewall for Snapdragon-powered PCs.**

Rakshak Edge inspects suspicious messages and entire conversation threads before a person acts. It combines deterministic security signals with a real local semantic classifier trained from the bundled multilingual corpus. Its conversation engine detects a scam's progression from identity setup to isolation and extraction. A production transformer can run through ONNX Runtime and the Qualcomm QNN Execution Provider. The complete reference app works fully offline, so judges can run the hybrid demo without downloading a model.

## Why this project matters

Scams exploit context, urgency, and trust. A cloud-only checker creates its own privacy problem because the user must upload the very message, account detail, or payment request they distrust. Rakshak Edge keeps analysis on the PC, explains every warning in plain language, and gives the user a safe next action.

## Product highlights

- Multilingual signal detection for English, Hinglish, and common Indian payment vocabulary
- URL analysis for look-alike domains, IP-address hosts, punycode, risky shorteners, and suspicious redirect parameters
- Financial entity extraction for UPI IDs, phone numbers, OTP language, currency amounts, and account references
- Evidence-first explanations instead of an opaque risk score
- Conversation intelligence that links harmless-looking turns into an explainable attack chain
- Privacy-safe incident reports that intentionally exclude the pasted source content
- A reproducible local language model with a fixed holdout evaluation set
- Local-only architecture with zero telemetry and an offline-ready web experience
- Snapdragon deployment adapter for ONNX Runtime QNN, with CPU fallback for development
- Accessible interface with keyboard navigation, high contrast, reduced motion support, and plain-language actions

## Quick start

```bash
python app.py
```

Open `http://127.0.0.1:8765`. No package installation or internet connection is required.

Run the tests:

```bash
python -m unittest discover -s tests -v
```

Reproduce the model evaluation:

```bash
python benchmarks/evaluate_model.py
```

Current checked-in result: **94.44% accuracy on an 18-message holdout set**, with all six high-risk and all six low-risk examples classified correctly. The intentionally small dataset proves the pipeline, not production readiness; the corpus and the single error are visible in the repository.

Reproduce the locked end-to-end challenge suite:

```bash
python benchmarks/evaluate_system.py
```

Current checked-in result: **97.78% accuracy across 45 balanced, non-training cases**. All 15 high-risk and all 15 medium-risk cases are correct. The one conservative false positive is printed by the evaluator rather than hidden.

Run a CLI analysis:

```bash
python -m engine.cli "KYC expires today. Share OTP and pay Rs 10 at http://secure-bank.example"
```

## Snapdragon path

On Snapdragon X Series Windows PCs, install the QNN-enabled ONNX Runtime package and place an INT8 text classifier at `models/scam_classifier.onnx`. Set `RAKSHAK_BACKEND=qnn`. Rakshak Edge asks ONNX Runtime for `QNNExecutionProvider`, then falls back to CPU when unavailable. See [docs/SNAPDRAGON_DEPLOYMENT.md](docs/SNAPDRAGON_DEPLOYMENT.md).

## Repository map

- `app.py`: zero-dependency local server and API
- `engine/`: message analyzer, conversation attack-chain engine, trained semantic classifier, URL analysis, entity extraction, and accelerator adapter
- `data/`: transparent multilingual corpus plus a locked 45-case system challenge suite
- `web/`: polished offline product UI
- `tests/`: deterministic safety regression suite
- `benchmarks/`: latency and quality harness
- `docs/`: architecture, deployment, threat model, demo script, and submission copy
- `submission/`: final brief and pitch deck files

## Privacy and safety

The default build makes no outbound requests. Analysis happens in memory, and the server stores no message history. Downloaded safety reports exclude the pasted source content. The product reports risk indicators and safer verification steps. It does not claim to prove that a message is genuine or fraudulent.

## License

MIT. See [LICENSE](LICENSE).
