# Model Scorecard — minimax-m3.1-flash-ollama-cloud-64kout

| Field | Value |
|---|---|
| **Date tested** | 2026-10-29 |
| **Model** | `minimax-m3.1-flash:cloud` |
| **Label** | `minimax-m3.1-flash-ollama-cloud-64kout` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/10 |
| Tasks (5) | **4/5** | passed: adherence, expense-tracker, kanban, reasoning · failed: fake-desktop |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **72.2 tok/s** | 4313 tokens in 59.7 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.1 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 429 | 22.5 |
| expense-tracker | ✓ | 51143 | 254.0 |
| fake-desktop | ✗ | 0 | 419.9 |
| kanban | ✓ | 98130 | 580.6 |
| reasoning | ✓ | 812 | 43.0 |

## Verdict

Measured profile: HE 19/20, Tasks 4/5, Agency 13/15, 72.2 tok/s, tool-call pass. Strength: code, throughput. Weakness: failed fake-desktop. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/minimax-m3.1-flash-ollama-cloud-64kout-testing-notes.md)
