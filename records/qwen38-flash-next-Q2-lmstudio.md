# Model Scorecard — qwen38-flash-next-Q2-lmstudio

| Field | Value |
|---|---|
| **Date tested** | 2026-10-17 |
| **Model** | `qwen3.8-flash-next-ud@q2_k_xl` |
| **Label** | `qwen38-flash-next-Q2-lmstudio` |
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
| Throughput | **38.2 tok/s** | 2172 tokens in 56.9 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 2.5 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 340 | 61.4 |
| expense-tracker | ✓ | 138147 | 725.5 |
| fake-desktop | ✓ | 130420 | 791.6 |
| kanban | ✓ | 10753 | 815.6 |
| reasoning | ✓ | 1735 | 145.9 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 15/15, 38.2 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/qwen38-flash-next-Q2-lmstudio-testing-notes.md)
