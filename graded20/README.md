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

## First scorecard — `Qwen3.8-27B-AWQ-5.0bpw` (2026-10-31)

Tiered result from a single 20-question pass, temperature 0, one attempt per question, 16,384-token
budget, served through an MLX/OpenAI-compatible endpoint on Apple Silicon.

| Tier | Passed | Items |
|---|---|---|
| easy | **4/5** | E5 wrong |
| normal | **4/5** | N2 wrong |
| hard | **3/5** | H1, H2 produced no answer |
| expert | **2/5** | X1, X2, X4 produced no answer |
| **total** | **13/20** | |

**15 of 20 answered; 13 of those 15 were correct (87%).** The other five never emitted code at all:
they spent the entire 16,384-token budget in reasoning (`finish_reason: length`, 29K–67K characters
of reasoning) and returned empty content. That is a real, reproducible property of this model on
specification-heavy tasks, not a harness artifact — the same five items came back empty at a 4,096
budget, and the fixed items (H4, X3) passed once the budget was raised.

Why this is reported as `no_answer` rather than a plain fail: merging the two would say the model is
"13/20" when it is *answered-15, correct-13, silent-5*. Those imply different work — one wants a
better prompt loop, the other wants a model that can finish a spec.

### Reproducibility notes

- Question set hash: `188a5816a338625f…` (see `suite_sha256` in each result file).
- Wall time: 33 min for the run; the five silent items consumed 26 of those minutes.
- A prior 4,096-budget pass is kept in `results/` as `…-20261031.json` (11/20). It is **not** the
  score — it is the evidence that an insufficient budget silently converts a thinking model into a
  non-answer, which is exactly the failure mode a benchmark must not hide.

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
