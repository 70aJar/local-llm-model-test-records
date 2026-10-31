# GRADED-20 — a stratified coding suite

A small, honest coding benchmark: **20 problems, 5 per difficulty tier**, each with a reference
solution and a deterministic test file.

## Why it exists

The flat 20-problem HumanEval slice we were running **saturated**: two models that are far apart in
real capability both scored a perfect 20/20, so the instrument reported "no difference, no progress"
night after night.

Cross-checked against the full 164-problem HumanEval suite (published by Luke's Dev Lab):

| Model | HE-20 (flat slice) | HE-164 (full suite) |
|---|---|---|
| `unsloth/Qwen3.8-27B` Q4_K_XL | 20/20 (100%) | 139/164 = **84.8%** |
| `ornith-ai/Ornith-1.5-35B-A3B` Q4_K_M | 20/20 (100%) | 117/164 = **71.3%** |

A 13.5-point gap collapsed into a tie. A pass rate hides *where* a model breaks; a tiered suite
shows it. That is the entire premise here.

## Structure

| Tier | IDs | What it asks for |
|---|---|---|
| easy | E1–E5 | string/list/dict basics, exact edge cases |
| normal | N1–N5 | a data structure or algorithm with a stated contract (LRU, RLE, merge intervals) |
| hard | H1–H5 | multi-part reasoning where a naïve implementation passes the easy assertions and fails the edge ones (Dijkstra with a lexicographic tie-break, C-style integer arithmetic, token bucket, linear-memory edit distance, stable topological order) |
| expert | X1–X5 | write a parser/engine from scratch (JSON, regex) or make code correct **under real concurrency** (SPSC ring buffer, racy counter) |

Every item states the exact required signature. The model sees only the prompt — never the tests.

## Honesty rules (please keep them)

1. **Frozen set.** The result JSON records `suite_sha256`; a published score is only comparable to
   runs over the same hash. Do not edit a question to make a model fail — that is not a benchmark.
2. **One attempt**, temperature 0 by default, no retries, no self-repair loop.
3. **Per-question matrix is published**, not just the tier total. With 5 items per tier, one
   question is 20% of that tier — a single flaky item is visible in the matrix and invisible in the
   summary.
4. **Validate before scoring.** `validate_suite.py` runs every reference solution against its own
   tests. A suite whose own solutions fail is measuring nothing.

## Run it

```bash
# prove the suite is sound (must print SUITE VALID)
python3 validate_suite.py

# score a model behind any OpenAI-compatible endpoint
python3 run_suite.py \
  --endpoint http://127.0.0.1:8000/v1/chat/completions \
  --model  my-model-id \
  --label  my-model-20260101
```

Output: `results/<label>.json` — label, model, endpoint class, temperature, suite hash, per-question
rows (seconds, pass, error, truncated answer), and tier totals.

## Scorecards — `Qwen3.8-27B-AWQ-5.0bpw` (2026-10-31)

Three passes, same frozen question set, temperature 0, one attempt per question, served through an
MLX/OpenAI-compatible endpoint on Apple Silicon.

| Tier | baseline | `reasoning_effort: ultra` | ultra, 2× budget (5 silent items only) |
|---|---|---|---|
| easy | 4/5 | **5/5** | — |
| normal | 4/5 | 4/5 | — |
| hard | 3/5 | 3/5 | 0/2 |
| expert | 2/5 | 2/5 | 0/3 |
| **total** | **13/20** | **14/20** | **0/5** |
| outcomes | 13 pass · 2 wrong · 5 silent | 14 pass · 6 silent | 5 silent |

**Ultra thinking is not a strict improvement.** It fixed E5 (wrong → pass, 120 s → 81 s) and broke N2
(pass → silent, 30 s → 388 s): raised effort made it over-deliberate on a task it previously solved
cheaply. Net +1 item, but the composition changed — 0 wrong, 6 silent.

### The five silent items are a termination limit, not a budget limit

They never emit code at any setting tried:

| Item | 16K budget | 32K budget |
|---|---|---|
| H1 Dijkstra + tie-break | 421 s, 64K chars reasoning | 823 s, **129K** chars reasoning |
| H2 expression evaluator | 310 s, 49K | 618 s, 113K |
| X1 JSON parser | 257 s, 34K | 383 s, 114K |
| X2 regex engine | 432 s, 63K | 423 s, 78K |
| X4 LCS diff script | 356 s, 51K | 731 s, 109K |

Doubling the budget roughly doubles the reasoning (H1: 64K → 129K characters) and still produces zero
code (`finish_reason: length`, empty content). An answer-now system directive — *"think at most three
sentences, then write the code, never end without code"* — changed nothing: the same five came back
empty. This model will consume whatever budget it is given on a task that requires constructing a whole
artifact, and will not commit to an answer.

Practical consequence: for this model, tier scores on construction-heavy problems are capped by
**termination**, not knowledge. A `no_answer` at a large budget is the finding.

### Reproducibility notes

- Question set hash: `188a5816a338625f…` (see `suite_sha256` in each result file).
- Wall time: baseline 33 min · ultra 45 min · ultra-at-32K 50 min (five items).
- Budget matters independently of effort: the very first pass at 4,096 is kept in `results/` as
  `…-20261031.json` (11/20) — seven of its nine failures were empty answers, not wrong code.


## Reading a score

- **Tier scores** tell you the shape: strong easy/normal + weak expert = a model that writes code
  but cannot hold a complex specification.
- **The matrix** tells you whether a score is real: the same question failing across runs is a
  capability gap; a question that flips between runs on identical settings is noise, and on a 5-item
  tier that noise is worth 20%.
- **Concurrency items (X3, X5) can be flaky on a heavily loaded machine.** A failure there is worth
  re-running once before it is believed — and if it only fails under load, that is a finding about
  the runtime, not the model.

## Licence / provenance

Question set and harness: MIT. Reference solutions are the author's own; no benchmark items were
copied from HumanEval, MBPP, or any other suite.
