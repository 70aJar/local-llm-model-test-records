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
| 2026-09-29 | **MiMo-VL-7B-RL-2508** (bartowski Q8_0, 9.5GB, `qwen2vl`) — A3b | LM Studio | **20/20** | 4/5⁶ | **14/15** | 16.7 | ✅ | [records/MiMo-VL-7B-RL.md](records/MiMo-VL-7B-RL.md) |
| 2026-09-29 | **MiMo-VL-7B-RL** (XiaomiMiMo BF16, 16.6GB, `qwen2vl`) — A3 | LM Studio | **20/20** | 4/5⁶ | 10/15 | 27.4 | ✅ | [records/MiMo-VL-7B-RL.md](records/MiMo-VL-7B-RL.md) |
| 2026-09-29 | **MiMo-V2.6-Distill-Qwen-9B-Ablitrated-i1** (Q6_K, 7.4GB) — A2 | LM Studio | 13/20 | **2/5**⁵ | 13/15 | 41.7 | ⚠️ intermittent⁷ | [records/MiMo-9B-Abliterated.md](records/MiMo-9B-Abliterated.md) |
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

⁵ **MiMo-9B-Abliterated — the 2/5 is NOT a capability score.** Four of the five tasks were **cut off
mid-generation**: it produced ~200,000 characters per task (expense-tracker 195K, fake-desktop 215K,
kanban 205K, reasoning 165K) and never terminated, burning the full 32K-token budget each time. Both of
its two "passes" came from truncated output that happened to contain code. Read this row as *failure to
terminate*, not as wrong code. It also carries a ⚠️ on tool-calling — see footnote ⁷.

⁶ **MiMo-VL tasks 4/5 — the failure is the same single task in both variants** (`adherence`), and both
completed the other four fully with no truncation (43K–74K chars). Both scored **20/20 HumanEval with
100% coverage**, equal to the best recorded here. **A3 and A3b are NOT the same weights**: `MiMo-VL-7B-RL`
(BF16) and `MiMo-VL-7B-RL-2508` (Q8_0) are **different checkpoints**, so this is not a precision A/B —
model revision and quant are confounded. A3b is 43% smaller yet 39% slower (16.7 vs 27.4 tok/s), which a
re-quant would not explain; the cause is unverified.

⁷ **MiMo-9B-Abliterated — tool-call channel is intermittent, and its failure mode is fabrication.** The
probe passed on one load (`tool_calls` → `lookup_employee({"name":"Sarah Chen"})`) and failed on another,
returning **no tool call** plus a fabricated record as prose:

```
{"employee_id": 1042, "first_name": "Sarah", "last_name": "Chen",
 "job_title": "Senior Accountant", "department": "Finance"}
```

It invented the result rather than calling the tool that would have looked it up. This is worse than a low
score: a plausible fabricated record raises nothing downstream. Its agency score is still 13/15 because the
scenarios did elicit real calls — the fault is intermittent, which is the hardest kind to catch. Compare
A1 Heretic on the same base family: 19/20 HE vs 13/20, 5/5 tasks vs runaway generation, and reliable tools.

---

### Vision suite — 602 items / 602 images, 6 benchmarks (seed 20260929)

Run separately from the battery above, **one VL model resident at a time**, `-c 65536`,
scored on accuracy only. Full method + grader corrections in the linked records.

| Benchmark | A1 Qwen3.5-9B | A3 MiMo-VL BF16 | A3b MiMo-VL-2508 Q8 | Chance |
|---|---|---|---|---|
| MMStar | **64.0%** | 61.0% | 58.0% | 25% |
| RealWorldQA | **77.0%** | 70.0% | 70.0% | 25% |
| OCRBench | **87.0%** | 79.0% | 73.0% | — |
| AI2D | 71.0% | 69.0% | **86.0%** | 25% |
| ChartQA | 75.0% | **77.0%** | 63.0% | — |
| POPE | 84.3% | **85.3%** | 83.3% | 50% |
| **Overall** | **460/602 = 76.4%** | 443/602 = 73.6% | 435/602 = 72.3% | — |

A **text-first 9B** model wins overall, ahead of two purpose-built VL models — and
**A1 wins 4 of 6 benchmarks**, with its biggest margins on OCRBench (+8/+14) and
RealWorldQA (+7), the benchmarks hardest to pass without genuinely reading the image.

The counter-example is what makes the table worth reading: **A3b beats A1 by 15 points
on AI2D** (science diagrams), and beat its own sibling by 17. No model leads everywhere;
the 3-way overall spread is 4.1 points while per-benchmark gaps reach 24. Pick on the
benchmark that matches your task, not on the total.

⚠️ **A1 requires ≥3072 output tokens** — it reasons before answering. At the 1536 default
it scored ~0% everywhere and looked blind (0 ch content, 4128 ch reasoning, `finish=length`).
It is not blind. **Probe and run must share one budget.**

⚠️ **Do not read the durations as model speed.** A1's run overlapped a neighbour model
loaded on demand by another app: 33–45 s/item with it resident, **20–21 s/item** without.
Accuracy is unaffected — the suite is accuracy-scored — but contended durations are not
performance figures.

[records/Vision-Suite-Qwen3.5-9B-Defiant-Fable.md](records/Vision-Suite-Qwen3.5-9B-Defiant-Fable.md) ·
[records/Vision-Suite-MiMo-VL.md](records/Vision-Suite-MiMo-VL.md)

---
*Every result is measured, wire-collected, and reproducible. If a row looks wrong,
open an issue — the harness is in this repo.*

