# Model Scorecard — lms-qwen38-27b-ridge-37bpw-h164

| Field | Value |
|---|---|
| **Date tested** | 2026-10-17 |
| **Model** | `qwen3.8-27b-ridge` |
| **Label** | `lms-qwen38-27b-ridge-37bpw-h164` |
| **Engine** | LM Studio |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **14/15** | failed: book_room_b |
| Throughput | **21.5 tok/s** | 3317 tokens in 154.4 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 3.8 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 361 | 504.4 |
| expense-tracker | ✓ | 114306 | 1733.3 |
| fake-desktop | ✓ | 109376 | 1771.6 |
| kanban | ✓ | 120160 | 1591.2 |
| reasoning | ✓ | 1183 | 358.9 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 14/15, 21.5 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/lms-qwen38-27b-ridge-37bpw-h164-testing-notes.md)
