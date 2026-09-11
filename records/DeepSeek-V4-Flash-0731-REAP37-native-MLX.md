# Model Scorecard — DeepSeek-V4-Flash-0731-REAP37-native-MLX

| Field | Value |
|---|---|
| **Date tested** | 2026-09-10 (fresh full battery) |
| **Model** | DeepSeek-V4-Flash-0731-REAP37-native-MLX (True2456, 96GB-class MoE) |
| **Engine** | oMLX (95.84 GiB resident) |
| **Host** | Apple Silicon M5 Max / 128 GB |
| **History** | Earlier partial tests suspected wrong math + ~6 tok/s; a fresh full battery corrects this |

## Results (full battery, thinking ON, AGENCY_TEMP 0.5, TASK_MAX_TOKENS 8000)
| Section | Score | Notes |
|---|---|---|
| HumanEval (HE20) | **13/20** | mid-tier code |
| Tasks (5) | **5/5** | adherence ✓ · expense-tracker ✓ (33KB) · fake-desktop ✓ (34KB) · kanban ✓ (30KB) · reasoning ✓ (all 3 correct: 17min bridge, 10-prisoner binary search, 1 pair) |
| Agency (15) | **13/15** | strong — room-booking tool-loop pattern only |
| Throughput | **26.0 tok/s** | 4× faster than earlier estimates (~6 t/s) |
| Tool-call | **OK** | schema-compliant {'a': 37, 'b': 15} |

## Verdict
- **CORRECTION to earlier notes**: the model is usable, not a stall-bomb.
- 26 tok/s, tool-calling OK, agency 13/15 → it earns a real position as a large,
  independent-MoE lane (96GB — FRIDAY-class nodes only).
- HE 13/20 is the honest ceiling: strong agent/tool behavior, mid code.
- Requires ~100GB reclaimable RAM: free LM Studio llama.cpp backends before loading
  (they hold 15-30GB invisible to `lms unload`).

---
Harness: `harness/full_test_model.py` | Data: `results/deepseek-v4-reap37-full.json`

> **Retested 2026-09-11 (reasoning):** initial Tasks grading used a code heuristic on a prose puzzle (harness bug) + 8K token cap that truncated mid-thought. Fixed grader + 32K budget → reasoning PASSES (17-min bridge, 10-prisoner binary, 1 pair). Tasks 4/5 → **5/5**. See harness reasoning grader fix.
