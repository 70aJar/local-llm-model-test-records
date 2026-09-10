# Model Scorecard — grug-27b-oQ8e-fp16

| Field | Value |
|---|---|
| **Date tested** | 2026-09-09 |
| **Model** | GRUG-27B (Qwen-class 27B, oQ8e + fp16, dense-equivalent) |
| **Source** | fleet oMLX (grug-27b-oQ8e-fp16) |
| **Quantization** | oQ8e-fp16 (28.56 GiB resident) |
| **Engine** | oMLX (`grug-27b-oQ8e-fp16`, batched) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | default |
| **GPU mode** | **High Power (fully utilized, 100% residency)** |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **17/20** | three problems failed |
| Tasks (5) | **4/5** | adherence ✓ · expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · reasoning ✗ |
| Agency (15) | **14/15** | one tool-skip (ticket_platform) |
| Throughput | **13.7 tok/s** | standalone, full-GPU |
| Tool-call | **OK** | schema-compliant {'a': 37, 'b': 15} |

## Notes
- **Full-GPU measurement**: system was switched to High Power mode; GPU at 100%
  residency. No tok/s spike vs non-boost → earlier model tok/s remain valid baselines.
- Tasks were **bounded** (TASK_MAX_TOKENS=8000 after a 32K uncapped run spent 57 min
  on one fake-desktop generation at 9.4 t/s) — GRUG writes long outputs.
- Dense Q8+fp16 27B: ~14 t/s even at full GPU — NOT the MoE speed class (Ornith
  oQ4e 67, Tiel 57).

## Verdict
Mid-tier worker: strong agency (14/15) and code (17/20), 4/5 tasks, but slow
dense-equivalent. Best for tool-loop/batch work where latency isn't critical;
not a speed pick.

---
Harness: `harness/full_test_model.py`
Data: `results/grug-27b-oq8e-bounded.json`.
