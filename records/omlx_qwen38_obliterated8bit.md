# Model Scorecard — omlx_qwen38_obliterated8bit

| Field | Value |
|---|---|
| **Date tested** | 2026-10-12 |
| **Model** | `Qwen3.8-27B-OBLITERATED-8bit` |
| **Label** | `omlx_qwen38_obliterated8bit` |
| **Engine** | oMLX |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **14/15** | failed: book_room_b |
| Throughput | **17.9 tok/s** | 6271 tokens in 351.2 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 4.9 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 342 | 356.7 |
| expense-tracker | ✓ | 111136 | 1974.5 |
| fake-desktop | ✓ | 94956 | 1991.7 |
| kanban | ✓ | 108375 | 1982.7 |
| reasoning | ✓ | 823 | 473.6 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 14/15, 17.9 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/omlx_qwen38_obliterated8bit-testing-notes.md)
