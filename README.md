# Local LLM Model Test Records

A living, reproducible record of local LLM tests. Every model we evaluate gets a
scorecard in `records/`, produced by the same battery and harness, so results are
comparable across models and over time. Add a model any time — no personal
information, no synthetic benchmarks, just real work.

## The battery (same for every model)

| Section | What it measures | Scale |
|---|---|---|
| **HumanEval** | Python code correctness (20 canonical problems) | 0-20 |
| **Tasks** | Real build tasks (adherence, expense-tracker, fake-desktop, kanban, reasoning) | 0-5 |
| **Agency** | Tool-calling scenarios — does the model follow the system/agent loop? | 0-15 |
| **Throughput** | Answer tokens/sec (standalone) | tok/s |
| **Tool-call** | Native tool-call/schema compliance | pass/fail |

Every model runs: **one engine at a time, standalone**, prompt-compatible harness
from `harness/`, thinking on/off per model card. Host: Apple Silicon M5 Max / 128 GB.

## Layout

```
├── README.md                → this file (methodology + index)
├── MODEL_SCORECARD.md.template
├── harness/
│   ├── full_test_model.py   → HE20 + Tasks5 + Agency15 + throughput + toolcall
│   ├── real_task_harness.py → 4 real-work tasks (invoice, grounded QA, summary, email)
│   └── requirements.txt
└── records/
    ├── Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md
    └── ...                   → one scorecard per tested model
└── notes/
    └── <MODEL>-testing-notes.md → harness config, raw observations, caveats
```

Every scorecard has a companion **testing-notes** file in `notes/` recording the exact harness
configuration, the raw per-item observations it was derived from, and the caveats that bound the
result. Read both before comparing two models.

## Datasets (all public)

| Dataset | Where | Used by |
|---|---|---|
| HumanEval (canonical gzip) | `openai/human-eval` on GitHub/HF | `full_test_model.py` → `HE_PATH` |
| 5 build-task prompts | `youtube-main/prompts/` (public repo) | `full_test_model.py` → `TASK_DIR` |

Point the harness at them with env vars, e.g.:
```bash
HE_PATH="/path/to/HumanEval.jsonl.gz" TASK_DIR="/path/to/prompts/" \
python3 harness/full_test_model.py "<engine-model-id>" "<label>"
```

## How to add a model

1. Load the model in the engine you're testing (LM Studio / oMLX / Ollama).
2. Run the battery:
   ```bash
   LM_API="http://127.0.0.1:1234/v1/chat/completions" \
   HE_N=20 python3 harness/full_test_model.py "<engine-model-id>" "<label>"
   ```
3. Copy `MODEL_SCORECARD.md.template` → `records/<MODEL>.md`, fill from the
 printed scorecard, add the results JSON from `benchmarks/results/`.
4. Add a companion `notes/<MODEL>-testing-notes.md`: exact harness config (engine, quant, context,
 env vars), the raw per-item observations behind each score, and the caveats. Use
 `notes/LFM2.5-2.6B-testing-notes.md` as the reference shape.
5. Add a row to the index table and open a PR.

## Index

| Date | Model | Engine | HE | Tasks | Agency | tok/s | Tool-call | Record |
|---|---|---|---|---|---|---|---|---|
| 2026-09-28 | **Qwen3.5-9B The Defiant Fable Uncensored Heretic NEO IMATRIX MAX MTP** (DavidAU, Q4_K_S, 8.4GB) | LM Studio | **19/20**³ | **5/5** | **15/15**⁴ | 51.9 | ✅ | [records/Qwen3.5-9B-Defiant-Fable.md](records/Qwen3.5-9B-Defiant-Fable.md) |
| 2026-09-28 | **LFM2.5-2.6B Turbo-Brilliance Power X12 NEO MAX** (DavidAU re-tune, Q8_0, 3.1GB) | LM Studio | **19/20**² | **4/5** | 12/15 | 82.5 | ✅ | [records/LFM2.5-2.6B-Turbo-Brilliance.md](records/LFM2.5-2.6B-Turbo-Brilliance.md) |
| 2026-09-11 | Gemma-4-31B-It-QAT-Uncensored-Heretic-MLX-LM-4Bit (31B MoE-class dense) | oMLX | 20/20 | 5/5 | 15/15 | 22.4 | ✅ | [records/Gemma-4-31B-It-QAT-Uncensored-Heretic-MLX-LM-4Bit.md](records/Gemma-4-31B-It-QAT-Uncensored-Heretic-MLX-LM-4Bit.md) |
| 2026-09-10 | DeepSeek-V4-Flash-0731-REAP37-native-MLX (96GB MoE) | oMLX | 13/20 | 5/5 | 13/15 | 26.0 | ✅ | [records/DeepSeek-V4-Flash-0731-REAP37-native-MLX.md](records/DeepSeek-V4-Flash-0731-REAP37-native-MLX.md) |
| 2026-09-10 | Qwen3.6-27B Fable-Fusion-711 (dequantized) | oMLX | smoke ✓ correctness | — | — | 1.6 | ✅ native JSON | [records/Qwen3.6-27B-Fable-Fusion-711-dequantized.md](records/Qwen3.6-27B-Fable-Fusion-711-dequantized.md) |
| 2026-09-10 | MiniCPM5-2B (BF16/8bit/4bit; XML protocol) | oMLX + LM Studio | 15-19/20 | 3-4/5 | 12-13/15 ✓ | 84.6-243.6 | 5/5 XML ✓ | [records/MiniCPM5-2B.md](records/MiniCPM5-2B.md) |
| 2026-09-09 | grug-27b-oQ8e-fp16 (full-GPU) | oMLX | 17/20 | 4/5 | 14/15 | 13.7 | ✅ | [records/grug-27b-oQ8e-fp16.md](records/grug-27b-oQ8e-fp16.md) |
| 2026-09-09 | Ornith-1.5-35B-A3B-oQ4e-fp16-mtp (22GB) | oMLX | 20/20 | 4/5 | 14/15 | 67.0 | ✅ | [records/Ornith-1.5-35B-A3B-oQ4e-mtp.md](records/Ornith-1.5-35B-A3B-oQ4e-mtp.md) |
| 2026-09-09 | google/gemma-4-26b-a4b-qat | LM Studio | 20/20 | 4/5 | 14/15 | 78.9 | ✅ | [records/Gemma-4-26B-QAT.md](records/Gemma-4-26B-QAT.md) |
| 2026-09-08 | gemma4-coding-agent (E4B Inst., Q4_K_M, Desktop GPU) | LM Studio (LM Link) | 19/20 | 5/5 | 15/15 | 77.8 | ✅ | [records/gemma4-coding-agent.md](records/gemma4-coding-agent.md) |
| 2026-09-08 | Tiel-Coder-35B-A3B-MTP-UD (Q4_K_XL, MTP) | LM Studio | 19/20 | 4/5 | 13/15 | 57.4 | ✅ | [records/Tiel-Coder-35B-A3B-MTP-UD.md](records/Tiel-Coder-35B-A3B-MTP-UD.md) |
| 2026-09-08 | Ornith-1.5-35B-A3B-MLX (bf16) | oMLX | 20/20 | 4/5 | 13/15 | 48.1 | ✅ | [records/Ornith-1.5-35B-A3B-MLX.md](records/Ornith-1.5-35B-A3B-MLX.md) |
| 2026-09-07 | Gemma-4-31B JANG_4M-CRACK (GGUF Q4/Q5/Q8) | LM Studio | 20/20 | 5/5 | 15/15 | 13.2 | ✅ | [records/Gemma-4-31B-JANG_4M-CRACK.md](records/Gemma-4-31B-JANG_4M-CRACK.md) |
| 2026-09-07 | google/gemma-4-31b-qat (Q4_0, vision) | LM Studio | 20/20 | 4/5 | 15/15 | 18.8 | ✅ | [records/Gemma-4-31B-QAT.md](records/Gemma-4-31B-QAT.md) |
| 2026-09-08 | gemma-4-12B-it-qat (4-bit MLX) | oMLX | 19/20 | 5/5 | 15/15 | 33.4 | ✅ | [records/gemma-4-12B-QAT.md](records/gemma-4-12B-QAT.md) |
| 2026-09-03 | Qwen3.8-27B GSQ-RCO IQ3_S-mtp (3.50 bpw) | LM Studio | 20/20 | 5/5 | 13/15 | 19.4 | ✅ | [records/Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md](records/Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md) |
| 2026-09-03 | MiniCPM-o-4.5 (MLX 4-bit) | oMLX | 15/20 | 5/5 | 6/15¹ | 95.4 | ✅ | [records/MiniCPM-o-4_5-MLX-4bit.md](records/MiniCPM-o-4_5-MLX-4bit.md) |

¹ Agency = 6/15 on strict name matching; intent was correct on 9 of the misses
(`employee_lookup`, `book_meeting_room`, `currency_conversion` etc.) — see scorecard.

² **LFM2.5-2.6B Turbo-Brilliance — read the scorecard before comparing this row.** The 19/20 was
measured with `{REASON:off}`. The same model, same quant, same host scored **0/20** under its default
mode with a harness that could not parse its Pythonic tool-call output format, and **11/20** once only
the parser was fixed. Six configurations are recorded (0, 11, 13, 15, 15, **19**). This is a deliberate
example of harness sensitivity, not a tuning trick — see `records/LFM2.5-2.6B-Turbo-Brilliance.md`.
Also note: **the modes HURT at 2.6B** (`off 19 > low 15 = medium 15 > high 11`); the author's card warns
the system scales with size, so this does not generalise to Turbo Brilliance as a method.

³ **Qwen3.5-9B Defiant Fable — 19/20 is the published figure across two full runs.** Run A (card's *general*
sampler, temp 1.0) scored 20/20; Run B (card's *coding* sampler, temp 0.6) scored 19/20. **19 of 20 items
pass in both runs** — only `HumanEval/10` moves. The 20/20 is recorded as an observed sample, not the score.
±1 on HE is this model's real variance; do not read 20 vs 19 as a capability difference.

⁴ **15/15 agency — perfect, and reproducible.** Identical across both runs with **zero** differing
scenarios. This model solves **both** halves of the room-booking pair (`book_room_a` + `book_room_b`),
which every other model we have tested fails at least one of, and `ticket_support_lead`, which failed all
six runs of the previous model. It also correctly **abstains** on the no-valid-tool restraint scenarios
instead of reaching for the `wiki_search` decoy. Agency is graded on tool selection rather than generated
code, so it is far less sampler-sensitive than HumanEval — this is the most trustworthy number in the row.

---
*Every result is measured, wire-collected, and reproducible. If a row looks wrong,
open an issue — the harness is in this repo.*

