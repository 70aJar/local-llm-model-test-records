# Model Scorecard — Lightning-30B-A3B-Q4_0

| Field | Value |
|---|---|
| **Date tested** | 2026-10-24 |
| **Model** | `ggml-org/nvidia-nemotron-3.5-lightning-30b-a3b-gguf/nvidia-nemotron-3.5-lightning-30b-a3b-q4_0.gguf` |
| **Label** | `Lightning-30B-A3B-Q4_0` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **4/5** | passed: adherence, expense-tracker, fake-desktop, kanban · failed: reasoning |
| Agency (15) | **13/15** | failed: book_room_b, ticket_support_lead |
| Throughput | **77.9 tok/s** | 2324 tokens in 29.8 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.9 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 417 | 65.8 |
| expense-tracker | ✓ | 50504 | 144.7 |
| fake-desktop | ✓ | 47889 | 151.3 |
| kanban | ✓ | 18697 | 153.4 |
| reasoning | ✗ | 9 | 80.3 |

## Verdict

Measured profile: HE 20/20, Tasks 4/5, Agency 13/15, 77.9 tok/s, tool-call pass. Strength: code, throughput. Weakness: failed reasoning. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Lightning-30B-A3B-Q4_0-testing-notes.md)
