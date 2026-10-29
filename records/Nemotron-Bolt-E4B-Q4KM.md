# Model Scorecard — Nemotron-Bolt-E4B-Q4KM

| Field | Value |
|---|---|
| **Date tested** | 2026-10-24 |
| **Model** | `nvidia-nemotron-3.5-bolt-e4b-4gb` |
| **Label** | `Nemotron-Bolt-E4B-Q4KM` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/17 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **12/15** | failed: book_room_b, ticket_support_lead, ticket_platform |
| Throughput | **24.6 tok/s** | 651 tokens in 26.5 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 3.1 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 449 | 60.4 |
| expense-tracker | ✓ | 22227 | 483.6 |
| fake-desktop | ✓ | 24826 | 425.9 |
| kanban | ✓ | 29980 | 451.7 |
| reasoning | ✓ | 1058 | 92.6 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 12/15, 24.6 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Nemotron-Bolt-E4B-Q4KM-testing-notes.md)
