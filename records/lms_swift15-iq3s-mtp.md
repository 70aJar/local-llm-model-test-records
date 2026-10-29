# Model Scorecard — lms_swift15-iq3s-mtp

| Field | Value |
|---|---|
| **Date tested** | 2026-10-14 |
| **Model** | `swift-1.5-qwen3.8-27b-gsq-rco` |
| **Label** | `lms_swift15-iq3s-mtp` |
| **Engine** | LM Studio |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **2/5** | passed: adherence, expense-tracker · failed: fake-desktop, kanban, reasoning |
| Agency (15) | **14/15** | failed: ticket_platform |
| Throughput | **37.8 tok/s** | 4638 tokens in 122.6 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.9 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 308 | 75.2 |
| expense-tracker | ✓ | 12621 | 835.9 |
| fake-desktop | ✗ | ? | ? |
| kanban | ✗ | ? | ? |
| reasoning | ✗ | ? | ? |

## Verdict

Measured profile: HE 20/20, Tasks 2/5, Agency 14/15, 37.8 tok/s, tool-call pass. Strength: code, agent/tool use. Weakness: failed fake-desktop, kanban, reasoning. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/lms_swift15-iq3s-mtp-testing-notes.md)
