# Rakshak Edge architecture

## Design goal

Rakshak Edge must deliver a useful answer when the PC is offline, keep sensitive content on the device, and show the evidence behind every warning. The system therefore uses a hybrid pipeline rather than a single generative model.

## Runtime flow

1. The local web app sends content only to `127.0.0.1`.
2. Entity extraction finds URLs, UPI handles, phone numbers, amounts, and credential terms.
3. The deterministic layer scores visible social-engineering patterns and URL structure.
4. The bundled word and character n-gram model adds semantic context locally.
5. The Snapdragon production profile can replace that compact reference model with an INT8 encoder through ONNX Runtime QNN.
6. A calibrated fusion layer combines both scores and keeps the top supporting evidence.
7. The response returns a risk band, plain-language evidence, and safe actions.
8. For a supplied conversation, the thread engine analyzes each turn and detects identity setup, isolation, and extraction across time.

## Production topology

```text
Local UI
  |
  v
Input boundary (size limit, no persistence)
  |
  +-- Entity and URL analyzer ------------------+
  |                                             |
  +-- Local semantic n-gram classifier          |
      Production: INT8 encoder -> QNN -> NPU    |
                                                v
                                  Evidence fusion and calibration
                                                |
                                                v
                                  Risk, reasons, safe action
                                                |
                           Conversation mode ---+
                           turn timeline + attack chain
```

## Why hybrid

Security decisions need traceable evidence. Rules catch crisp, high-risk facts such as a raw-IP link or an OTP request. The checked-in compact classifier handles paraphrases and mixed language today. The rule layer also supplies a dependable fallback when a model or accelerator is unavailable.

## Data boundary

- No database
- No cloud model
- No analytics SDK
- No third-party font or JavaScript request
- No raw message history in local storage or on the server
- Exported reports omit the pasted source content
- API binds to loopback by default

## Model contract

The checked-in reference classifier uses multinomial Naive Bayes over word, word-bigram, and character n-gram features. It trains deterministically from 72 transparent examples and is evaluated on a fixed 18-message holdout. The production classifier accepts token IDs and an attention mask and produces logits for `low`, `medium`, and `high`. The recommended NPU candidate is a MobileBERT-class encoder fine-tuned on a larger consented and synthetic Indian scam corpus, exported to ONNX, statically quantized to INT8, and compiled or profiled for Snapdragon through Qualcomm AI Hub.

## Evaluation contract

The model holdout measures only the semantic classifier. A separate locked 45-case suite measures the complete rules-plus-model product. The suite is balanced across low, medium, and high risk and never participates in training. `benchmarks/evaluate_system.py` prints every error and the full confusion matrix.

## Failure behavior

- If QNN is unavailable, ONNX Runtime uses CPU.
- If the model is absent, the transparent rule engine remains fully functional.
- If content is empty or exceeds the input limit, the server rejects it before analysis.
- The UI never labels a message as proven safe. A low score means no strong pattern was found.
