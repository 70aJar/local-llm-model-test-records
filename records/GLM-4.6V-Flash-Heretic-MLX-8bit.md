# Model Scorecard — GLM-4.6V-Flash-Heretic-MLX-8bit

| Field | Value |
|---|---|
| **Date tested** | 2026-10-07 |
| **Model** | `GLM-4.6V-Flash-Heretic-MLX-8bit` |
| **Label** | `GLM-4.6V-Flash-Heretic-MLX-8bit` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **14/20** | failed: HumanEval/0, HumanEval/1, HumanEval/4, HumanEval/6, HumanEval/10, HumanEval/15 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **12/15** | failed: list_support_platform, ticket_support_lead, ticket_platform |
| Throughput | **43.2 tok/s** | 886 tokens in 20.5 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 2.0 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 402 | 24.6 |
| expense-tracker | ✓ | 3635 | 307.2 |
| fake-desktop | ✓ | 76848 | 962.4 |
| kanban | ✓ | 78420 | 912.0 |
| reasoning | ✓ | 54890 | 927.0 |

## Verdict

Measured profile: HE 14/20, Tasks 5/5, Agency 12/15, 43.2 tok/s, tool-call pass. Strength: build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/GLM-4.6V-Flash-Heretic-MLX-8bit-testing-notes.md)
