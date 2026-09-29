# MiMo-VL-7B-RL — A3 (BF16) and A3b (2508, Q8_0)

**Verdict: A3b (2508) is the strongest sub-10B all-rounder tested so far. A3 is
weaker than its size suggests.**

⚠️ **These are NOT the same weights at two precisions.** I initially described this
as a clean quant A/B — it is not. They are different checkpoints:

| | A3 | A3b |
|---|---|---|
| LM Studio key | `mimo-vl-7b-rl` | `xiaomimimo_mimo-vl-7b-rl-2508` |
| Source | `XiaomiMiMo/MiMo-VL-7B-RL` | bartowski `..._MiMo-VL-7B-RL-2508` |
| Quant / size | BF16 · 16.62 GB | Q8_0 · 9.47 GB |
| Architecture | `qwen2vl` + mmproj | `qwen2vl` + mmproj |

The `2508` is a **separate, later checkpoint**. Any difference below is
model-revision + quant combined and cannot be attributed to precision alone.

## Results

| Section | A3 (BF16) | A3b (2508 Q8_0) |
|---|---|---|
| HumanEval | **20/20** | **20/20** |
| Agency | 10/15 | **14/15** |
| Tasks | 4/5 | 4/5 |
| Throughput | **27.4 tok/s** | 16.7 tok/s |
| Tool call | ✅ emitted (52 correct) | ✅ emitted (52 correct) |
| Coverage | 20/20 · 15/15 · 5/5 | 20/20 · 15/15 · 5/5 |

Both scored a **clean 20/20 HumanEval with full coverage** — equal to the best in
the fleet records, and slightly above A1's published 19/20.

Both failed the same single task (`adherence`) and both passed the other four
with fully answered, untruncated output (43K–74K chars).

## The anomaly worth flagging

**A3b is 43% smaller yet 39% slower** (9.47 GB / 16.7 tok/s vs 16.62 GB / 27.4 t/s).
A smaller quant of identical weights should be *faster*, not slower. Combined with
the agency gap, this is consistent with 2508 being a genuinely different (heavier)
architecture revision rather than a re-quant of the same graph.

**I have not proven the cause.** Candidate explanations, untested:
- 2508 is a different architecture revision with more compute per token
- vision-token handling differs between the two mmproj files
- a serving-side difference in how LM Studio loaded the two

Until one is confirmed, treat the speed figure as measured-but-unexplained rather
than as a property of the checkpoint.

## Agency detail

| Scenario | A3 | A3b |
|---|---|---|
| dept_lookup | P | P |
| list_active_eng | **F (no call)** | P |
| count_eng | P | P |
| list_support_platform | P | P |
| book_room_b | **F (check_avail, never book)** | **P (booked)** |
| book_room_a | **F** | **F (check_avail, never book)** |
| check_room_b | **F (no call)** | P |
| ticket_manager | P | P |
| ticket_support_lead | P | P |
| ticket_platform | P | P |
| convert_eur_usd | P | P |
| convert_usd_jpy | P | P |
| restraint_thanks | **F (spurious call)** | P |
| restraint_weather | P | P |
| focus_team | P | P |

A3's failures are mostly **not calling at all** (`list_active_eng`, `check_room_b`)
plus one **spurious call** (`restraint_thanks` — called `get_exchange_rate` on a
plain thank-you, i.e. over-eager tool use).

A3b fixed every one of those except `book_room_a` — the *check-availability-then-
never-book* pattern, which is the recurring family trait across the fleet's small
models and appears in A2 as well.

## Recommendation

- **A3b (2508)** — deploy. Best sub-10B text+tool profile measured: perfect
  HumanEval with full coverage, 14/15 agency, 4/5 tasks.
- **A3 (BF16)** — do not deploy over A3b. Equal HumanEval, materially worse
  agency (10 vs 14), and 1.75× the disk for no measured gain.

## Vision

Both are VL models, but **this battery is text-only.** Vision capability is
claimed by the model card, not verified here — it is being measured separately by
the vision suite (MMStar / RealWorldQA / OCRBench / AI2D / ChartQA / POPE,
602 items) via `run_vision_batch.py`.
