# Model Scorecard — gemma-4-12B (QAT 4-bit)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-06 |
| **Model** | gemma-4-12B-it-qat-4bit |
| **Source** | mlx-community QAT 4-bit |
| **Quantization** | 4-bit QAT (mlx) |
| **Size on disk** | 11.0 GB |
| **Engine** | oMLX (OpenAI-compatible :8002) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 262,144 (full window) |
| **Thinking** | OFF (default) |

## Context benchmark (oMLX)

| Metric | Value |
|---|---|
| Context applied | 262,144 (full window) |
| Verified prefill | 262,144 |
| Prefill speed | **265.4 tok/s** |
| Duration | 1013.6 s (16.9 min) |

Best full-window dense prefill measured so far in this series.

## Results (thinking OFF)

| Section | Score | Details |
|---|---|---|
| Agency (15) | **15/15** | PERFECT — every tool call correct, no decoys, both restraint cases clean |
| Agentic Coding (3) | **3/3** | multi-file Flask app (4.0K chars, 96.7s) · refactor (40.5s) · bug-fix (56.0s) |
| Tool-call | **OK** | schema-compliant, {'a': 37, 'b': 15}, 1.7s |

## Agency highlights

- All 15 scenarios clean: employee lookup, directory filters, room booking,
  availability checks, ticket creation (multi-chain), currency conversion
  (multi-tool chains), both restraint cases (no tool call), focus re-query.
- No `wiki_search` decoy usage anywhere.
- Tool-name adherence is exact (unlike MiniCPM's synonym drift).

## Agentic coding highlights

- **multi_file_app**: produced a complete 3-file Flask project (app.py +
  models.py + utils.py, /health + POST /items with validation) — 4,003 chars
  in 96.7s.
- **refactor**: dataclass conversion, dedup preserved behavior — 1,625 chars.
- **fix_bug**: identified the duplicate-reporting bug with a working fix —
  1,824 chars.

## Verdict

A tiny (11 GB) 12B model that is **perfect on agentic tool-use with thinking
OFF at 265 tok/s prefill**. First perfect 15/15 agency score in this series.
Strong candidate for chat + light coding on modest hardware. Thinking-ON
comparison is queued.

---
Harness: `harness/full_test_model.py` · raw JSON in `results/gemma-4-12b-qat-agentic2330.json`.
Compare: [MiniCPM-o-4.5 MLX](MiniCPM-o-4_5-MLX-4bit.md) — the tool-name-drift
profile; [Qwen3.8-27B GSQ-RCO](Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md) — elite HE,
terrible verbosity.