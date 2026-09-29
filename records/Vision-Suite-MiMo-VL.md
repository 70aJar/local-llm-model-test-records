# Vision Suite — MiMo-VL 7B (RL and 2508)

**Date:** 2026-09-29
**Suite:** 602 items / 602 images across 6 benchmarks (seed 20260929)
**Served by:** LM Studio `:1234`, one model resident at a time, `-c 65536`
**Location:** `/Volumes/AIPortable/AI Server/Vision Benchmarks/`

Two MiMo-VL-7B checkpoints, **not** a quant pair — `MiMo-VL-7B-RL` (BF16) and
`...-2508` (Q8_0) are different revisions, so nothing here isolates precision.

## Results

| Benchmark | A3 BF16 | A3b Q8_0 | Chance |
|---|---|---|---|
| MMStar | 61/100 = **61.0%** | 58/100 = **58.0%** | 25% |
| RealWorldQA | 70/100 = **70.0%** | 70/100 = **70.0%** | 25% |
| OCRBench | 79/100 = **79.0%** | 73/100 = **73.0%** | — |
| AI2D | 69/100 = **69.0%** | 86/100 = **86.0%** | 25% |
| ChartQA | 77/100 = **77.0%** | 63/100 = **63.0%** | — |
| POPE | 87/102 = **85.3%** | 85/102 = **83.3%** | 50% |
| **Overall** | **443/602 = 73.6%** | **435/602 = 72.3%** | — |

**The two checkpoints are effectively tied overall (1.3 pts) but disagree sharply
per benchmark** — A3 leads OCRBench (+6), ChartQA (+14) and POPE (+2); A3b leads
AI2D (+17). A single overall number hides that; use the per-benchmark split.

A3b is 43% smaller (9.47 GB vs 16.62 GB) yet **slower in vision too** (13.6 s/item
on AI2D vs 10.5 s), matching its text-battery behaviour (16.7 vs 27.4 tok/s). A
size reduction that costs speed as well as quality on both axes is worth flagging
before anyone assumes "smaller quant = cheaper, same thing".

## Two measured corrections — read before quoting any MiMo-VL number

**1. AI2D is re-graded (0-based).** The first pass scored AI2D **8/100 (A3)** and
**28/100 (A3b)** — *below* the 25% guessing floor, which is impossible for a model
answering honestly and was the tell. AI2D's `answer` field is a **0-based index**
into `options` (proven by a `0` appearing: counts `{0:27, 1:29, 2:26, 3:18}`); the
grader assumed 1-based and guarded with `1 <= gold <= len(opts)`, so every `gold≥1`
item mapped to the **wrong option** and every `gold=0` item fell through to text
matching. Re-run with the fixed grader: **69/100** and **86/100**.

This shifted both overalls by ~10 points (A3 63.5% → 73.6%; A3b 62.6% → 72.3%).
The uncorrected figures are void and must not be quoted.

**2. A1's first "cannot see" verdict was a harness bug, not a model limit.**
`Qwen3.5-9B-Defiant-Fable` reported `PROBE-FAILED / empty content` on a 1024-token
probe. It was not blind — it spent the budget reasoning. Measured directly:

| `max_tokens` | `finish_reason` | `content` | `reasoning_content` |
|---|---|---|---|
| 1024 | `length` | **0 ch** | 4128 ch |
| 3072 | `stop` | **`C`** | 5139 ch |

`C` is the correct answer. A1 needs ≥3072 tokens to emit an answer; the probe ran
it at 1024. **The probe now shares one budget with the run** — never probe with
less than you score with, or a verbose reasoner reads as blind.

## Method notes that keep these numbers honest

- **Extraction:** answer read from `content` only; `<think>…</think>` stripped first;
  an unclosed `<think>` counts as no answer; empty content is a genuine failure.
  `reasoning_content` is **never** graded — chain-of-thought is not an answer.
- **`\boxed{}`** unwrapped (last box wins); yes/no normalised; MCQ by letter.
- **Recovery rule:** if stripping `<think>` leaves content empty *and* the raw text
  contains a `\boxed{}`, that box is taken as the answer (an explicit marker, not
  prose) and the record is tagged.
- **POPE is sampled 34/34/34** across adversarial/popular/random. The dataset is
  category-ordered in blocks, so a naive 3,000-row cap returns **100% adversarial**
  — a harder slice that would have been published as "POPE".
- **Re-gradability:** results store the think-stripped answer *and* raw text, so a
  grader fix replays over stored data instead of forcing a re-run.

## Reproduce

```bash
cd ~/Projects/AlitaAICore/benchmarks
VISION_MAX_TOKENS=4096 /usr/bin/python3 run_vision_batch.py A1   # heavy reasoner
/usr/bin/python3 run_vision_batch.py                            # all models
/usr/bin/python3 merge_ai2d_fix.py                              # splice re-grade
```

Raw results: `benchmarks/results/vision-A3*-CORRECTED.json`, plus the untouched
original runs and `-ai2d-rerun.json` so the bug and its fix both stay auditable.
