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
- **Verbosity problem**: adherence produced a 116K-char prompt echo (371 fake bullets) — grader hardened to catch (>20K chars = fail). Real build tasks also verbose (fake-desktop 104K, reasoning 78K chars) but code-correct.
- Passes reasoning ✓, fails adherence ✗ — inverted profile vs most models.

## Verdict
Fast, smart (20/20 HE), but runaway verbosity needs output caps for real use — especially for a strict-format task like adherence. With max_tokens caps it's a strong mid-size worker; uncapped it's a token furnace.

---
Harness: `harness/full_test_model.py`
Data: `results/gemma4-26b-qat-full.json`.
