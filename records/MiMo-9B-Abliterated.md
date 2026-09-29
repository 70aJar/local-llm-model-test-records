# MiMo-9B-Abliterated-i1 (Q6_K) — A2

**Verdict: NOT RECOMMENDED as an agent.** Unreliable tool-call channel that
fabricates tool output, and it does not terminate on open-ended tasks.

## Identity

| | |
|---|---|
| LM Studio key | `mimo-v2.6-distill-qwen-9b-ablitrated-i1` |
| Quant / size | Q6_K · 7.36 GB (mradermacher i1) |
| Architecture | `qwen35` (`Qwen3_5ForConditionalGeneration`) |
| Context | 262,144 native; loaded `-c 65536` |
| Lineage | `Qwen3.5-9B-Base → MiMo-V2.6-Distill-Qwen-9B → Abliterated` |
| Card samplers | *(none published)* — ran the A1 set: temp 0.6 / top_p 0.95 / top_k 20, task+agency temp 1.0 |

## Results

| Section | Score | Valid? |
|---|---|---|
| HumanEval | **13/20** | yes (19/20 answered, 1 truncated) |
| Agency | **13/15** | yes (15/15 answered) |
| Tasks | **2/5** | ❌ **INVALID — 4 of 5 truncated** |
| Throughput | 41.7 tok/s | yes |
| Tool call | emitted ✅ (37+15=52 correct) | yes |

**Do not quote "2/5" as a task score.** Four of five tasks were cut off
mid-generation; 2 of the 2 "passes" came from truncated output that happened to
contain code.

## Why the Tasks score is invalid — runaway generation

| Task | Chars generated | Secs | Answered |
|---|---|---|---|
| adherence | 546 | 5.4 | answered |
| expense-tracker | **195,387** | 819 | truncated |
| fake-desktop | **214,737** | 843 | truncated |
| kanban | **205,339** | 820 | truncated |
| reasoning | **165,436** | 815 | truncated |

It generated ~200,000 characters per task and never stopped — every one burned the
full 32K-token budget. For comparison, A3b completed the *same* tasks in 43K–74K
characters. This is a **failure to terminate**, not wrong code.

> Note: an earlier run of these tasks returned repeated HTTP 400s. That was a
> *separate* harness bug (`TASK_MAX_TOKENS=32000` against a 32768 context, so
> prompt + max_tokens always exceeded the window) and was fixed before this run
> with a CTX guard. It is not the cause of the truncation above — this run had a
> 65,536 context and never hit the guard.

## The serious finding — fabricated tool output

The tool-call gate probe was run on two separate loads of this model:

| Probe | Result |
|---|---|
| first load | ✅ `tool_calls` populated → `lookup_employee({"name":"Sarah Chen"})` |
| second load | ❌ **no tool call at all** |

The second probe returned:

```
content='{"employee_id": 1042, "first_name": "Sarah", "last_name": "Chen",
         "job_title": "Senior Accountant", "department": "Finance"}'
```

**It invented an employee record instead of calling the tool that would have
looked one up.** The tool-call channel is unreliable, and its failure mode is
confident fabrication rather than an admission it did not call.

This matters more than the score: a plausible fabricated record is worse than a
refusal, because nothing downstream flags it. The agency section still scored
13/15 because the scenarios there did elicit real calls — so this is an
*intermittent* fault, which is the hardest kind to catch in production.

## Agency detail (13/15)

Failed: `book_room_a`, `book_room_b` — called `check_availability` and then never
booked. Same family trait seen in other sub-10B models.

## Comparison — abliteration vs Heretic on one base family

Same battery, same base family (`Qwen3.5-9B-Base`), differing only in how refusal
was removed:

| | A1 Heretic (Defiant Fable) | A2 Abliterated |
|---|---|---|
| HumanEval | **19/20** | 13/20 |
| Agency | **15/15** | 13/15 |
| Tasks | **5/5** | 2/5 (4 truncated) |
| tok/s | **51.9** | 41.7 |
| Tool call | reliable | **intermittent + fabricates** |

Heretic-style decensoring clearly preserves more capability than diff-in-means
abliteration here. The gap in HumanEval (19 vs 13) and termination behaviour is
large enough to matter.

## Recommendation

Do not route agent or tool work to A2. If the abliterated variant is wanted for
unguarded chat, it is usable — but it should not be given tools, and long
generations must be capped with a hard token limit and a stop condition.
