# Model Scorecard — A3b-MiMo-VL-7B-RL-2508-Q8_0

| Field | Value |
|---|---|
| **Date tested** | 2026-09-29 |
| **Model** | `xiaomimimo_mimo-vl-7b-rl-2508` |
| **Label** | `A3b-MiMo-VL-7B-RL-2508-Q8_0` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **4/5** | passed: expense-tracker, fake-desktop, kanban, reasoning · failed: adherence |
| Agency (15) | **14/15** | failed: book_room_a |
| Throughput | **16.7 tok/s** | 4366 tokens in 262.2 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 5.9 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✗ | 2107 | 11.1 |
| expense-tracker | ✓ | 43723 | 246.2 |
| fake-desktop | ✓ | 42385 | 351.1 |
| kanban | ✓ | 74193 | 662.9 |
| reasoning | ✓ | 25640 | 351.9 |

## Verdict

Measured profile: HE 20/20, Tasks 4/5, Agency 14/15, 16.7 tok/s, tool-call pass. Strength: code, agent/tool use. Weakness: failed adherence. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/A3b-MiMo-VL-7B-RL-2508-Q8_0-testing-notes.md)
