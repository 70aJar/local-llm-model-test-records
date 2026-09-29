# Vision Suite — Qwen3.5-9B-Defiant-Fable (the generalist wins)

**Date:** 2026-09-29
**Suite:** 602 items / 602 images across 6 benchmarks (seed 20260929)
**Served by:** LM Studio `:1234`, one model resident at a time, `-c 65536`
**Location:** `/Volumes/AIPortable/AI Server/Vision Benchmarks/`
**Budget:** `VISION_MAX_TOKENS=4096` — this model reasons before answering

## Headline

A **text-first 9B** model beats two purpose-built MiMo-VL-7B vision models on
vision. **A1 460/602 = 76.4%**, ahead of A3 BF16 (73.6%) and A3b Q8_0 (72.3%) —
+2.8 and +4.1 points.

## Results — all three models

| Benchmark | A1 Qwen3.5-9B | A3 MiMo-VL BF16 | A3b MiMo-VL-2508 Q8 | Chance |
|---|---|---|---|---|
| MMStar | **64/100 = 64.0%** | 61.0% | 58.0% | 25% |
| RealWorldQA | **77/100 = 77.0%** | 70.0% | 70.0% | 25% |
| OCRBench | **87/100 = 87.0%** | 79.0% | 73.0% | — |
| AI2D | 71/100 = 71.0% | 69.0% | **86.0%** | 25% |
| ChartQA | 75/100 = 75.0% | **77.0%** | 63.0% | — |
| POPE | 86/102 = 84.3% | **87/102 = 85.3%** | 85/102 = 83.3% | 50% |
| **Overall** | **460/602 = 76.4%** | 443/602 = 73.6% | 435/602 = 72.3% | — |

**A1 wins four of six benchmarks**, and its margins are largest where vision is
hardest to fake: OCRBench **+8/+14** (dense text extraction) and RealWorldQA
**+7** (photographic scenes). It does not win by guessing — the gaps are on
capabilities that require actually reading the image.

## The exception is the interesting part

**A3b beats A1 by 15 points on AI2D** (86 vs 71), and beat its own sibling A3 by
17. AI2D is science **diagrams** — labelled, structured, arrow-and-caption figures.
A 15-point gap is far too large to be noise at n=100.

So the honest reading is not "A1 is the best vision model". It is:

- **A1 is the best generalist** — natural images, scene text, charts.
- **A3b has a real, specific strength on structured diagrams** that neither A1 nor
  A3 shares. Why the *smaller, later* MiMo checkpoint (9.47 GB) beats the BF16
  one (16.62 GB) by 17 points on diagram parsing is unexplained by this suite.

Anyone picking a model for diagram/document parsing should test A3b on their own
data before defaulting to the higher overall score.

## Per-benchmark ranking matters more than the total

| Rank | MMStar | RealWorldQA | OCRBench | AI2D | ChartQA | POPE |
|---|---|---|---|---|---|---|
| 1st | **A1** 64 | **A1** 77 | **A1** 87 | **A3b** 86 | **A3** 77 | **A3** 85.3 |
| 2nd | A3 61 | A3/A3b 70 | A3 79 | A1 71 | A1 75 | A1 84.3 |
| 3rd | A3b 58 | — | A3b 73 | A3 69 | A3b 63 | A3b 83.3 |

No model leads everywhere. The 3-way overall spread is only 4.1 points while the
per-benchmark spread is up to 24 (AI2D) and 23 (OCRBench) — **publishing only the
total would discard the decision-relevant information.**

## Reading this model correctly: it reasons before it answers

A1 is a heavy reasoner on *every* item. Measured behaviour:

| `max_tokens` | `finish_reason` | `content` | `reasoning_content` |
|---|---|---|---|
| 1024 | `length` | **0 ch** | 4128 ch |
| 3072 | `stop` | **`C`** (correct) | 5139 ch |

At a 1536-token budget (the harness default tuned for MiMo-VL) this model scored
**~0% on every benchmark and produced a false "cannot see" verdict.** It is not
blind — it spends the budget thinking and then answers. **Probe and run must share
one budget**, or a verbose reasoner reads as blind. Suite ran at 4096.

Cost of that reasoning: **~2× the wall-clock of MiMo-VL** (see below).

## Throughput caveat — do not quote the durations as model speed

A1's run overlapped a neighbour model loaded by another app (its `fast` scoring
lane, JIT-loaded on demand from its own config default). Measured directly:

| window | A1 rate |
|---|---|
| neighbour resident | 33–45 s/item |
| neighbour unloaded | **20–21 s/item** |

Roughly a **2× contention penalty**. It does **not** affect any score above —
the suite is accuracy-scored, and the neighbour's traffic was separated
unambiguously by request shape (harness sends 1 message; the app sends 2) and by
per-model request counts in the engine log (460 under the A1 key vs 10 under the
neighbour). Only the recorded per-benchmark `secs` are inflated. **Never quote a
contended duration as a throughput figure.**

## Method

- **Extraction:** `content` only; `<think>…</think>` stripped first; unclosed
  `<think>` = no answer; empty content = genuine failure. `reasoning_content` is
  **never** graded.
- **`\boxed{}`** unwrapped (last box wins); recovered even from inside `<think>` and
  tagged; yes/no normalised; MCQ by letter.
- **POPE sampled 34/34/34** across adversarial/popular/random — the dataset is
  category-ordered in blocks, so a naive cap returns 100% adversarial.
- **Re-gradable:** both the think-stripped answer and raw text are stored, so a
  grader fix replays over stored data. A1: **602 items, 0 errors**.

## Reproduce

```bash
cd ~/Projects/AlitaAICore/benchmarks
VISION_MAX_TOKENS=4096 /usr/bin/python3 run_vision_batch.py A1
/usr/bin/python3 run_vision_batch.py            # all models
```

Raw results: `benchmarks/results/vision-A1-Qwen3.5-9B-Defiant-Fable.json`.
MiMo-VL pair: `records/Vision-Suite-MiMo-VL.md`.
