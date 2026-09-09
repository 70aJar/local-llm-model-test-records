# Model Scorecard — google/gemma-4-31b-qat (Q4_0)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-07 |
| **Model** | google/gemma-4-31b-qat (Gemma-4 31B Instruct, QAT-quantized GGUF) |
| **Source** | [google/gemma-4-31b-qat](https://huggingface.co/google/gemma-4-31b-qat) / LM Studio community build |
| **Quantization** | Q4_0 (17.56 GiB) |
| **Engine** | LM Studio (`google/gemma-4-31b-qat`, type=vlm, vision=true) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 128K (`-c 131072`) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | perfect |
| Agency (15) | **15/15** | perfect — no tool-loop drops |
| Throughput | — | reasoning-on runs |
| Tool-call | **OK** (7.3s) | schema-compliant |

## Notes & quirks

- **Vision: TRUE and verified.** This is the vision-capable 31B (mmproj ships as
  `mmproj-gemma-4-31B-it-QAT-BF16.gguf`, 1.2 GB). Real image test passed: fed a
  screenshot of a model-benchmark dashboard, model correctly described it.
- **Thinking baked in** — same Gemma-4 behavior as CRACK; `enable_thinking`
  ignored by LM Studio, reasoning emitted natively. Runs at temp 0.5.
- Safe counterpart to the CRACK variant: identical 20/20 + 15/15, with guardrails
  intact. Its mmproj is the donor for the CRACK vision graft (copy + index-cache
  clear + restart → CRACK sees images too).
- No vision/reasoning markers were stripped by the conversion (unlike CRACK).

## Verdict

The "safe lane" 31B: perfect HE + agency, real working vision out of the box.
Use it anywhere guardrails matter (public-facing, client work); use the CRACK
variant when refusal-free behavior is needed. Capability parity confirms the
abliteration cost nothing on our battery.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
Data: `results/gemma4-31b-qat-agency.json`, `results/gemma4-31b-qat-humaneval.json`.