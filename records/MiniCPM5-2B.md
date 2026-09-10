# Model Scorecard — MiniCPM5-2B (MLX 4-bit + MLX 8-bit)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-10 |
| **Model** | MiniCPM5-2B (OpenBMB, released 2026-09-07) |
| **Family** | MiniCPM5 dense 2B, native 128K ctx |
| **Engines** | LM Studio (MLX 4-bit affine) + oMLX (MLX 8-bit) |
| **Host** | Apple Silicon M5 Max / 128 GB |

## Results — MLX 4-bit (LM Studio lane)
| Section | Score |
|---|---|
| HumanEval (HE20) | 15/20 |
| Tasks (5) | 3/5 (3 degenerate 130-156K loops) |
| Agency (15) | 2/15 |
| Throughput | 243.6 tok/s |
| Tool-call | NO |

## Results — MLX 8-bit (oMLX lane)
| Section | Score |
|---|---|
| HumanEval (HE20) | **18/20** |
| Tasks (5) | **4/5** (bounded, clean) |
| Agency (15) | **2/15** (unchanged) |
| Throughput | 164.5 tok/s |
| Tool-call | **NO** |

## Verdict
- **8-bit quant fixes code quality** (HE 15→18, tasks clean) but **NOT agentic ability**
- Agency 2/15 + no tool call on BOTH quants → **model-level trait**, not quantization
- **NOT deployed to fleet** — our small-node lane needs tool discipline; E4B (15/15 agency, 77.8 t/s) and GSQ-RCO (13/15, 19.4 t/s) already outperform at similar footprints
- Best use: blazing-fast pure-answer/edge tasks where tool-calling isn't needed

---
Harness: `harness/full_test_model.py` | Data: `results/minicpm5-2b-mlx-full.json`, `results/minicpm5-2b-mlx-8bit-full.json`
