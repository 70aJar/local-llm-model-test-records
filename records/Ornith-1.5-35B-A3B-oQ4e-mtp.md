# Model Scorecard — Ornith-1.5-35B-A3B-oQ4e-fp16-mtp (22 GB)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-09 |
| **Model** | Ornith-1.5-35B-A3B oQ4e-fp16-mtp (4-bit MoE + fp16 + MTP head) |
| **Source** | ornith-ai/Ornith-1.5-35B-A3B-MLX (oQ4e quant in oMLX) |
| **Quantization** | oQ4e-fp16 (22 GB, ~21.24 GB resident) |
| **Engine** | oMLX (`Ornith-1.5-35B-A3B-oQ4e-fp16-mtp`, engine=vlm) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 262K capable |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | perfect |
| Tasks (5) | **4/5** | expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · adherence ✓ (grader fix) · reasoning ✗ |
| Agency (15) | **14/15** | better than fp16's 13/15 — booked one room |
| Throughput | **67.0 tok/s** | standalone |
| Tool-call | **OK** | schema-compliant |

## Verdict
**The daily-driver quant for the 35B-A3B class.** Same 20/20 HE as fp16, BETTER
agency (14/15), 39% faster (67 vs 48 tok/s), at ⅓ the memory (22 GB vs 65 GB).
If you run one Ornith, run this one.

---
Harness: `harness/full_test_model.py`
Data: `results/ornith-oq4e-mtp-full.json`.
