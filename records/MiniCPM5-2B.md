# Model Scorecard — MiniCPM5-2B (BF16 ORIGINAL + MLX 4-bit + MLX 8-bit)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-10 |
| **Model** | MiniCPM5-2B (OpenBMB, 2026-09-07) — 2,516,756,480 params, 42 layers, GQA 16Q/2KV, 131K ctx |
| **Official card claim** | 2B-class SOTA incl. "advantages in tool use and agentic tasks" |
| **Engines** | oMLX (BF16 original + MLX 8-bit) · LM Studio (MLX 4-bit) |
| **Host** | Apple Silicon M5 Max / 128 GB |

## Results (all three precisions — full battery each)

| Section | BF16 original (5.03GB) | MLX 8-bit (oMLX) | MLX 4-bit (LM Studio) |
|---|---|---|---|
| HumanEval (HE20) | **19/20** | 18/20 | 15/20 |
| Tasks (5) | 3/5 | 4/5 | 3/5 |
| Agency (15) | **2/15** | 2/15 | 2/15 |
| Throughput | 84.6 tok/s | 164.5 tok/s | 243.6 tok/s |
| Tool-call | **NO** | NO | NO |

## Verdict
- **The agentic weakness is the MODEL, not the quantization.** Full BF16 precision
  gives best-in-family code quality (19/20 HE) but agency stays 2/15 and tool-call
  fails at every precision tested.
- Official card's "tool use / agentic tasks SOTA" does NOT reproduce through the
  OpenAI-compatible function-calling layer (oMLX + LM Studio both).
- **NOT deployed as fleet agent.** Best use: fast pure-answer/edge coding (19/20 HE
  at 84.6 t/s), no tool-calling expected.
- oMLX benchmark note: bf16 decode ~88-91 tok/s at pp4096, ~42-88 at pp1024
  depending on context profile; continuous batching ~linear (1.87x@2, 3.62x@4).

---
Harness: `harness/full_test_model.py` | Data: `results/minicpm5-2b-bf16-original-full.json`
