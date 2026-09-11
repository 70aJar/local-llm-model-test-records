# Model Scorecard — Qwen3.6-27B-Fable-Fusion-711 (dequantized)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-10 (smoke probe) |
| **Model** | symrex/Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-NEO-MAX-MTP-GGUF-dequantized |
| **Engines** | oMLX (vlm engine, 52.00 GiB resident) |
| **Host** | Apple Silicon M5 Max / 128 GB |

## Measured (live smoke probe)
| Probe | Result |
|---|---|
| Code task decode | **1.6 tok/s** (315.5s for 500 tokens) |
| Code correctness | ✅ correct approach (prime-number function, structured reasoning) |
| Reasoning quality | ⚠️ verbose "Thinking Process:" wall leaked into `content` (not `reasoning_content`); hit token cap mid-answer |
| Tool-call | ✅ **Perfect native OpenAI JSON**: `{"name":"add","arguments":"{\"a\": 37, \"b\": 15}"}` (`call_c3bd0d59`) |
| Tool latency | 75.8s |

## Context from fleet marathons (earlier)
- Sep 2 real-task run: 4/4 passes but invoice took **1,473s (24.5 min)** with thinking ON
- Sep 3: **0.9 tok/s** in the 27B-family slow tier
- Full HE/Agency battery: never completed — would take ~8-14h at this speed

## Verdict
- **NOT adopted for fleet work.** Same 27B Fable-Fusion/Heretic lineage is excellent, but this
  **GGUF-dequantized 52GB build runs at ~1-1.6 tok/s** — every task is minutes-to-hours.
- Native JSON tool-calling works perfectly (no XML protocol quirks like MiniCPM5).
- The 20GB MLX sibling (`qwen3.6-27b-coder-mlx`) carries the same lineage at **20.4 tok/s,
  15/15 agency, 5/5 tasks** — use that for real work.
- Kept in oMLX catalog as MTP/spec-decode + identity-LoRA coder-lane reference.

---
Data: smoke probe 2026-09-10 (code + tool), oMLX log attribution verified.
