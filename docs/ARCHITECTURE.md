# Rakshak Edge architecture

## Design goal

Rakshak Edge must deliver a useful answer when the PC is offline, keep sensitive content on the device, and show the evidence behind every warning. The system therefore uses a hybrid pipeline rather than a single generative model.

## Runtime flow

1. The local web app sends content only to `127.0.0.1`.
2. Entity extraction finds URLs, UPI handles, phone numbers, amounts, and credential terms.
3. The deterministic layer scores visible social-engineering patterns and URL structure.
4. The optional INT8 classifier adds semantic context through ONNX Runtime.
5. A calibrated fusion layer combines both scores and keeps the top supporting evidence.
6. The response returns a risk band, plain-language evidence, and safe actions.

## Production topology

```text
Local UI
  |
  v
Input boundary (size limit, no persistence)
  |
  +-- Entity and URL analyzer ------------------+
  |                                             |
  +-- INT8 text classifier                      |
      ONNX Runtime -> QNN EP -> Hexagon NPU     |
                                                v
                                  Evidence fusion and calibration
                                                |
                                                v
                                  Risk, reasons, safe action
```

## Why hybrid

Security decisions need traceable evidence. Rules catch crisp, high-risk facts such as a raw-IP link or an OTP request. A compact classifier handles paraphrases and mixed language. The rule layer also supplies a dependable fallback when a model or accelerator is unavailable.

## Data boundary

- No database
- No cloud model
- No analytics SDK
- No third-party font or JavaScript request
- Browser history remains in local storage only when that feature is enabled
- API binds to loopback by default

## Model contract

The production classifier accepts token IDs and an attention mask and produces logits for `benign`, `suspicious`, and `high-risk`. The recommended candidate is a MobileBERT-class encoder fine-tuned on consented and synthetic Indian scam examples, exported to ONNX, statically quantized to INT8, and compiled or profiled for Snapdragon through Qualcomm AI Hub.

## Failure behavior

- If QNN is unavailable, ONNX Runtime uses CPU.
- If the model is absent, the transparent rule engine remains fully functional.
- If content is empty or exceeds the input limit, the server rejects it before analysis.
- The UI never labels a message as proven safe. A low score means no strong pattern was found.
