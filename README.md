# Rakshak Edge

**A private, on-device social-engineering firewall for Snapdragon-powered PCs.**

Rakshak Edge inspects suspicious messages, payment requests, QR payloads, and links before a person acts. It combines deterministic security signals with an optional compact language model that can run through ONNX Runtime and the Qualcomm QNN Execution Provider. The reference app works fully offline and ships with a deterministic fallback, so judges can run the demo without downloading a model.

## Why this project matters

Scams exploit context, urgency, and trust. A cloud-only checker creates its own privacy problem because the user must upload the very message, account detail, or payment request they distrust. Rakshak Edge keeps analysis on the PC, explains every warning in plain language, and gives the user a safe next action.

## Product highlights

- Multilingual signal detection for English, Hinglish, and common Indian payment vocabulary
- URL analysis for look-alike domains, IP-address hosts, punycode, risky shorteners, and suspicious redirect parameters
- Financial entity extraction for UPI IDs, phone numbers, OTP language, currency amounts, and account references
- Evidence-first explanations instead of an opaque risk score
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

Run a CLI analysis:

```bash
python -m engine.cli "KYC expires today. Share OTP and pay Rs 10 at http://secure-bank.example"
```

## Snapdragon path

On Snapdragon X Series Windows PCs, install the QNN-enabled ONNX Runtime package and place an INT8 text classifier at `models/scam_classifier.onnx`. Set `RAKSHAK_BACKEND=qnn`. Rakshak Edge asks ONNX Runtime for `QNNExecutionProvider`, then falls back to CPU when unavailable. See [docs/SNAPDRAGON_DEPLOYMENT.md](docs/SNAPDRAGON_DEPLOYMENT.md).

## Repository map

- `app.py`: zero-dependency local server and API
- `engine/`: risk engine, URL analysis, entity extraction, and accelerator adapter
- `web/`: polished offline product UI
- `tests/`: deterministic safety regression suite
- `benchmarks/`: latency and quality harness
- `docs/`: architecture, deployment, threat model, demo script, and submission copy
- `submission/`: final brief and pitch deck files

## Privacy and safety

The default build makes no outbound requests. Analysis happens in memory and history stays in the browser's local storage. The product reports risk indicators and safer verification steps. It does not claim to prove that a message is genuine or fraudulent.

## License

MIT. See [LICENSE](LICENSE).
