# Snapdragon deployment guide

## Target

- Snapdragon X Series HP PC
- Windows 11 on Arm
- ONNX Runtime with Qualcomm QNN Execution Provider
- INT8 ONNX text classifier

The QNN Execution Provider enables ONNX Runtime to execute supported graphs through Qualcomm's accelerator backend on Snapdragon devices. Prebuilt Windows packages include QNN support in current ONNX Runtime releases.

## Model preparation

1. Fine-tune a MobileBERT-class encoder for three labels: benign, suspicious, and high-risk.
2. Export with a fixed sequence length of 128 or 256 tokens.
3. Apply static INT8 quantization with a representative calibration set that includes English, Hinglish, and transliterated Indian-language scams.
4. Use Qualcomm AI Hub to profile the model on a Snapdragon X device and inspect unsupported operators.
5. Save the final artifact as `models/scam_classifier.onnx`.

## Runtime selection

```powershell
$env:RAKSHAK_BACKEND="qnn"
python app.py
```

The adapter requests providers in this order:

```python
["QNNExecutionProvider", "CPUExecutionProvider"]
```

Use `onnxruntime.get_available_providers()` to confirm QNN appears on the target PC. The API should report the active provider in its metadata after the classifier is integrated.

## Optimization choices

- INT8 weights and activations reduce memory traffic and suit NPU execution.
- Fixed sequence shapes avoid recompilation across requests.
- Tokenization stays on CPU while the transformer encoder runs on the NPU.
- The deterministic URL and entity layer remains on CPU because it finishes in sub-millisecond time on typical PCs.
- Cache the QNN context binary after first load to reduce subsequent startup time.

## Acceptance checks on target hardware

- QNN appears as the first active provider.
- Warm analysis latency stays below 100 ms for a 128-token message.
- The process makes no outbound network connection during analysis.
- CPU fallback produces the same label contract.
- Twenty repeated runs keep the UI responsive and do not increase memory continuously.

## Primary technical references

- ONNX Runtime QNN Execution Provider: https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html
- Qualcomm AI Hub: https://aihub.qualcomm.com/
- Snapdragon X Elite product brief: https://docs.qualcomm.com/bundle/publicresource/87-71417-1_REV_D_Snapdragon_X_Elite_Product_Brief.pdf
