# Model Scorecard — Defiance-27B-IQ4XS-MTP

| Field | Value |
|---|---|
| **Date tested** | 2026-10-24 |
| **Model** | `qwen3.8-27b-defiance-uncensored-mtp@iq4_xs` |
| **Label** | `Defiance-27B-IQ4XS-MTP` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **26.7 tok/s** | 8000 tokens in 299.4 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 3.4 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 437 | 148.7 |
| expense-tracker | ✓ | 47366 | 495.8 |
| fake-desktop | ✓ | 47237 | 599.1 |
| kanban | ✓ | 52282 | 573.9 |
| reasoning | ✓ | 972 | 175.9 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 15/15, 26.7 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Defiance-27B-IQ4XS-MTP-testing-notes.md)
