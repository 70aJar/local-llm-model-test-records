# Model Scorecard — gemma-4-12B-it-qat (4-bit MLX, QAT)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-08 (full battery), 2026-09-06 (agency/prefill) |
| **Model** | gemma-4-12B-it-qat-4bit |
| **Source** | mlx-community QAT 4-bit |
| **Quantization** | 4-bit QAT (MLX) |
| **Size on disk** | ~11 GB |
| **Engine** | oMLX (`gemma-4-12B-it-qat-4bit`) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 262K capable |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | one problem failed |
| Tasks (5) | **5/5** | adherence ✓ (grader fix) · expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · reasoning ✓ |
| Agency (15) | **15/15** | perfect — no tool-loop drops |
| Throughput | **33.4 tok/s** | standalone |
| Tool-call | **OK** | schema-compliant |

## Notes & quirks

- **One of only two models (with E4B coding-agent) strong on BOTH axes**: 5/5 Tasks
  AND 15/15 Agency — the 31B Gemmas trade reasoning-task for perfect agency, the
  A3B family trades agency for speed; 12B QAT keeps both at 33 tok/s.
- **Prefill speed**: 265.4 tok/s verified at 262K full window (context benchmark,
  oMLX) — best full-window dense prefill in the series.
- Thinking OFF by default on oMLX; clean, fast agentic behavior.

## Verdict

The balanced Gemma: perfect agency, perfect tasks, good HE, fast prefill. If the
fleet needs one mid-size model that can be trusted in tool loops AND build tasks
without model-switching, this is the strongest single pick under 35B.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
Data: `results/gemma-4-12b-qat-full.json`.
