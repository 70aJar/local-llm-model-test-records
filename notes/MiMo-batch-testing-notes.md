# MiMo batch (A2 / A3 / A3b) — testing notes

Exact conditions so these numbers can be reproduced or disputed.

## What was run

`run_mimo_batch.py` — sequential, **one model resident at a time**. Each model:
`lms unload --all` → `lms load <key> --yes -c 65536` → tool-call gate probe →
`full_test_model.py` battery (HumanEval 20 · Tasks 5 · Agency 15 · tool call).

| Label | LM Studio key | Quant | Size |
|---|---|---|---|
| A2 | `mimo-v2.6-distill-qwen-9b-ablitrated-i1` | Q6_K | 7.36 GB |
| A3 | `mimo-vl-7b-rl` | BF16 | 16.62 GB |
| A3b | `xiaomimimo_mimo-vl-7b-rl-2508` | Q8_0 | 9.47 GB |

Command: `cd ~/Projects/AlitaAICore/benchmarks && /usr/bin/python3 run_mimo_batch.py`
Master log: `…/logs/mimo-batch-20260929_014413.log`
Battery logs: `…/logs/battery-A{2,3,3b}-*.log`
JSON: `benchmarks/results/A{2,3,3b}-*.json`

## Samplers

No published sampler set on either card, so the **A1 set** was applied:

```
TEMP=0.6  TASK_TEMP=1.0  AGENCY_TEMP=1.0
TOP_P=0.95  TOP_K=20  MIN_P=0.0  REP_PEN=1.0
HE_N=20  CTX_TOKENS=65536
```

Context **65,536** (not 32768). Reasoning below.

## Two harness bugs found and fixed BEFORE these numbers

### 1. max_tokens could not fit in the context (fixed)

`run_tasks()` requests `TASK_MAX_TOKENS=32000`. With models loaded at `-c 32768`,
**prompt + max_tokens always exceeded the window**, so the server rejected task
requests with **HTTP 400** — which presents as a model failure.

This retroactively explains a stray HTTP 400 that A1 hit on expense-tracker and
which was earlier waved off as a transient. It was not a transient.

Fix — CTX guard in `full_test_model.py`:

```python
_ctx = int(os.environ.get("CTX_TOKENS", "32768"))
_budget = _ctx - (len(prompt) // 4) - 512
if mt > _budget:
    print(f"    [ctx-guard] {t}: max_tokens {mt} -> {_budget}")
    mt = max(1024, _budget)
```

plus `CTX_TOKENS=65536` and `-c 65536` in the runner. **A model's loaded context
and the harness's max_tokens must be checked together, not independently.**

### 2. The model runner supports a tool-call gate (kept)

Before each battery the runner probes the tool-call wire format, because a model
that emits XML tool calls and a server that does not translate them scores 0/15
agency while producing perfect calls in its own format (this is what happened to
MiniCPM5-2B). A gate failure now means "the wiring is wrong", not "the model is
bad". It flagged A2 on this run — see below.

## A2 — what the scores do and do not mean

**Tasks 2/5 is not a capability score.** 4 of 5 tasks were **truncated**:

| Task | Chars | Secs | Answered |
|---|---|---|---|
| adherence | 546 | 5.4 | answered |
| expense-tracker | 195,387 | 819 | **truncated** |
| fake-desktop | 214,737 | 843 | **truncated** |
| kanban | 205,339 | 820 | **truncated** |
| reasoning | 165,436 | 815 | **truncated** |

~200,000 chars per task with no termination, burning the full 32K token budget
each time. Both "passes" came from truncated output that happened to contain
code. This is a **failure to terminate**. A3b completed the same tasks in
43K–74K chars.

**Tool-call channel is intermittent and fabricates.** Two loads of the same model:

- load 1 — probe **passed**: `tool_calls` → `lookup_employee({"name":"Sarah Chen"})`
- load 2 — probe **failed**: no tool call; returned a fabricated record as prose
  (`employee_id 1042, Sarah Chen, Senior Accountant, Finance`)

It invented the tool's output rather than calling the tool. Graded on 15
scenarios the model still scored 13/15 because calls did occur there — the fault
is intermittent.

## A3 vs A3b — the comparison is confounded (correction)

**These are not the same weights at two precisions.** The keys differ:

```
mimo-vl-7b-rl            → XiaomiMiMo/MiMo-VL-7B-RL
xiaomimimo_mimo-vl-7b-rl-2508 → bartowski ..._MiMo-VL-7B-RL-2508
```

`2508` is a separate, later checkpoint. Model revision and quant are confounded,
so no difference can be attributed to precision alone.

Unresolved anomaly: **A3b is 43% smaller yet 39% slower** (9.47 GB @ 16.7 tok/s vs
16.62 GB @ 27.4 tok/s). A re-quant of identical weights should be faster. Causes
are not established; candidates include a heavier 2508 architecture revision, a
different mmproj/vision-token path, or a serving-side difference. Recorded as
measured-but-unexplained.

## Agency — per scenario

| Scenario | A2 | A3 | A3b |
|---|---|---|---|
| dept_lookup | P | P | P |
| list_active_eng | P | **F (no call)** | P |
| count_eng | P | P | P |
| list_support_platform | P | P | P |
| book_room_b | F | F | **P** |
| book_room_a | F | F | **F** |
| check_room_b | P | **F (no call)** | P |
| ticket_manager | P | P | P |
| ticket_support_lead | P | P | P |
| ticket_platform | P | P | P |
| convert_eur_usd | P | P | P |
| convert_usd_jpy | P | P | P |
| restraint_thanks | P | **F (spurious call)** | P |
| restraint_weather | P | P | P |
| focus_team | P | P | P |

`book_room_a` is the recurring family trait — models call `check_availability` and
then never book. A3b is the only model here that books in *any* room scenario.

## Cross-model comparison (same battery)

| Model | HE | Tasks | Agency | tok/s | Tool call |
|---|---|---|---|---|---|
| A1 Qwen3.5-9B Defiant Fable (Heretic) | 19/20 | 5/5 | **15/15** | 51.9 | reliable |
| A2 MiMo-9B-Abliterated | 13/20 | 2/5† | 13/15 | 41.7 | **intermittent + fabricates** |
| A3 MiMo-VL-7B-RL (BF16) | 20/20 | 4/5 | 10/15 | 27.4 | ✅ |
| A3b MiMo-VL-7B-RL-2508 (Q8_0) | **20/20** | 4/5 | **14/15** | 16.7 | ✅ |

† invalid — truncation, see above.

A1 and A2 share the base family (`Qwen3.5-9B-Base`), differing only in how refusal
was removed. Heretic-style decensoring preserved markedly more capability than
diff-in-means abliteration: HE 19 vs 13, tasks 5/5 vs runaway generation, and
reliable vs intermittent tool use.

## Vision — separate, not in these numbers

A3/A3b are VL models but **this battery is text-only**. Vision is claimed by the
card, not verified here. Measured separately by `run_vision_batch.py` against the
602-item suite (MMStar / RealWorldQA / OCRBench / AI2D / ChartQA / POPE). A model
that cannot actually receive an image is recorded as **unverified, not scored** —
a load succeeding does not prove the mmproj is attached.
