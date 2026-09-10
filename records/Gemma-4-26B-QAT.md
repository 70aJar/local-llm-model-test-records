# Model Scorecard — google/gemma-4-26b-a4b-qat

| Field | Value |
|---|---|
| **Date tested** | 2026-09-09 |
| **Model** | Gemma-4 26B A4B Instruct (QAT) |
| **Source** | google/gemma-4-26b-a4b-qat |
| **Quantization** | QAT MLX (14.57 GiB) |
| **Engine** | LM Studio (`google/gemma-4-26b-a4b-qat`) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 128K |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | perfect |
| Tasks (5) | **4/5** | expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · reasoning ✓ · adherence ✗ (runaway verbosity: 116K-char prompt echo) |
| Agency (15) | **14/15** | one booking missed |
| Throughput | **78.9 tok/s** | standalone |
| Tool-call | **OK** | schema-compliant |

## Notes
- A4B MoE: 78.9 tok/s at 26B total — very fast dense-equivalent.
- **VERBOSITY FIXED (Sep 9)**: default greedy temp (0.2) causes late-onset degenerate repetition loops (399 repeated chunks in fake-desktop, 104-116K chars, length-capped). Card sampling (temp 0.5 + repeat-penalty 1.2) eliminates it: same fake-desktop prompt → 20.6K chars, 0 repeats, natural stop. Harness now supports TASK_TEMP / TASK_REP_PEN. 26B needs these settings for build tasks.
- Passes reasoning ✓, fails adherence ✗ — inverted profile vs most models.

## Verdict
Fast, smart (20/20 HE), but runaway verbosity needs output caps for real use — especially for a strict-format task like adherence. With max_tokens caps it's a strong mid-size worker; uncapped it's a token furnace.

---
Harness: `harness/full_test_model.py`
Data: `results/gemma4-26b-qat-full.json`.
