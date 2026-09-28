# Model Scorecard — LFM2.5-2.6B Turbo-Brilliance Power X12 NEO MAX (DavidAU re-tune)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-28 |
| **Model** | `DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` — a re-tune of `LiquidAI/LFM2.5-2.6B` |
| **Base** | LFM2.5-2.6B — 2.69B dense, 30 layers (22 double-gated short-conv + 8 GQA), 131K ctx, 34T pretrain tokens |
| **Source** | [Hugging Face](https://huggingface.co/DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF) (public, Apache-2.0, not gated) |
| **Quantization** | **Q8_0** (~3.12 GB) — the card states Q8 is 1.5–2× stronger than Q6 |
| **Engine** | LM Studio `:1234` (llama.cpp backend) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | **131,072** (full) — verified via `/api/v0/models` `loaded_context_length` |

> **Naming note:** despite the `Qwen3.8` token in the name, **this is not a Qwen model.** The base is
> LiquidAI's LFM2.5-2.6B; "Qwen3.8" refers to the *reasoning-control methods* the author adapted
> ("The methods used in Qwen 3.8 27B to control/adjust reasoning were in part what inspired this project").

## Results — the benchmark changes the answer (read this first)

The headline is that **the same model scores 0/20 or 19/20 on HumanEval depending entirely on harness
configuration**, with no change to the weights, the quant, or the hardware. Six runs, one engine, one
host:

| Run | `{REASON:…}` | Samplers | HumanEval | Tasks | Agency | tok/s | Tool-call |
|---|---|---|---|---|---|---|---|
| BASELINE | *(none → default `high`)* | temp 0.2, no top_k/min_p/top_p | **0/20** | 3/5 | 12/15 | 101.9 | ✅ |
| D | *(none → default `high`)* | + unwrapper | **11/20** | 3/5 | 12/15 | 97.5 | ✅ |
| E | `low` | temp 0.2 | 15/20 | 2/5 | 11/15 | 83.0 | ✅ |
| A | `medium` | temp 0.2 | 15/20 | 2/5 | 12/15 | 104.3 | ✅ |
| B | `medium` | temp 1 / top_k 64 / min_p .05 / top_p .95 | 13/20 | 3/5 | 12/15 | 98.8 | ✅ |
| **C** | **`off`** | temp 0.2 | **19/20** | **4/5** | 12/15 | 82.5 | ✅ |

Answer coverage was **20/20 · 15/15 · 5/5 in every run** — nothing truncated, nothing skipped, so every
number above is a genuine measurement rather than a budget artifact.

### Why the baseline was 0/20 — two independent bugs, neither sufficient alone

1. **The harness could not parse the model's native output format.** Because LFM2.5 was RL-trained
   *inside* real agent harnesses, "complete the following Python function" is answered with a **Pythonic
   tool call**, not a markdown code block:
   ```
   <|tool_call_start|>[stateful_python_code_exec(code='def has_close_elements(...): ...')]<|tool_call_end|>
   ```
   The code inside is **correct**. `extract_code()` scraped the wrapper text and scored FAIL on all 20.
   Verified by dumping raw responses for `HumanEval/0` under `medium` vs `off`: same correct algorithm,
   different wrapper only.
2. **The run silently used the model's heaviest default mode.** The card states defaults are **`high` for
   reasoning, `medium` for instruct**, so a bare user message is *not* a neutral baseline — it is the
   "maximise thoroughness" mode applied to a five-line function.

**Decomposition:** parser fix alone `0 → 11/20`; mode fix on top `11 → 19/20`. Fixing only one still
misrepresents the model (11/20 or 0/20).

## Results (published configuration — `{REASON:off}`)

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | full 20/20 coverage |
| Tasks (5) | **4/5** | adherence ✓ · expense-tracker ✗ · fake-desktop ✓ · kanban ✓ · reasoning ✓ |
| Agency (15) | **12/15** | 15/15 coverage — see breakdown |
| Throughput | **82.5 tok/s** | standalone (`{REASON:off}` writes 23–29K-char outputs on build tasks) |
| Tool-call | **pass** | `{'a': 37, 'b': 15}` |

### Agency breakdown (12/15)

```
dept_lookup            PASS  ['lookup_employee']
list_active_eng        PASS  ['search_directory']
count_eng              PASS  ['search_directory']
list_support_platform  PASS  ['search_directory','search_directory']
book_room_b            FAIL  ['check_availability']      ← checked, never booked
book_room_a            PASS  ['book_room']
check_room_b           PASS  ['check_availability']
ticket_manager         PASS  ['lookup_employee']
ticket_support_lead    FAIL  ['lookup_employee']
ticket_platform        FAIL  ['lookup_employee']
convert_eur_usd        PASS  ['convert_currency']
convert_usd_jpy        PASS  ['convert_currency']
restraint_thanks       PASS  []
restraint_weather      PASS  []
focus_team             PASS  ['lookup_employee']
```

**Agency 12/15 is configuration-invariant** — identical under `off`, `medium` and the default `high`
(only `low` drops to 11/15, via an over-called `wiki_search` on the no-tool `restraint_weather`
scenario). This is the most trustworthy number on the card: a flat **12/15 for a 2.6B model**, one point
off the 35B-A3B family's 13/15.

## Notes & quirks

- **Thinking is always on and cannot be disabled.** The model card states LFM2.5 is "a pure reasoning
  model that always thinks before it answers — it adds a `<think>` tag directly in the chat template."
  `enable_thinking:false` and `reasoning_effort:low` are therefore **ignored by design**, not by a
  serving bug. Plan the token budget around reasoning (~85–92% of completion tokens in the default mode).
- **Tool-call protocol:** LFM2.5 emits **Pythonic** calls (`<|tool_call_start|>[fn(k=v)]<|tool_call_end|>`)
  by default; OpenAI-style JSON is only produced when the **system prompt asks for it**. LM Studio
  translated for us here so `tool_calls` came back clean, but a JSON-only harness should not be trusted
  to judge this family without reading `chat_template.jinja` first.
- **The Turbo-Brilliance modes HURT at this parameter count.** Ordered by HumanEval:
  `off 19 > low 15 = medium 15 > high 11`; Tasks `off 4/5` vs 2–3/5 for every mode. The author's own
  tester samplers made HE worse again (13/20). **Operational recommendation: run this model with
  `{REASON:off}`.** ⚠️ This is a **2.6B-specific** result — the card warns the system scales with size
  ("9B, 27B => will be a LOT stronger"), so it should **not** be generalised to the method itself.
- **Throughput caveat:** ~83–104 tok/s measured vs the card's 220 tok/s on M5 Max. The card quotes the
  *stock LiquidAI* model; this is a re-tune under LM Studio with thinking always on. Treat it as a floor.
  `{REASON:off}` is slowest only because it writes much longer outputs, not because the engine is slower.

## Verdict

> **A genuinely strong 2.6B edge agent — and a case study in how easily a benchmark can lie.** It scores
> **19/20 HumanEval, 12/15 agency and clean tool-calls at ~3 GB**, which puts it one agency point off the
> 35B-A3B family at a fraction of the size; LiquidAI's "RL-trained inside real agent harnesses" claim
> holds up. But it also produced a **confident 0/20 HumanEval verdict** on the identical model twenty
> minutes earlier — caused solely by a harness that could not read its output format, compounded by a
> default reasoning mode we never suspected existed. Neither bug was visible from the outside: low score
> plus full answer-coverage looks exactly like a capability gap.
>
> The transferable lesson outranks the score: **read a model's chat template and model card before you
> score it, and when a result is catastrophically low, keep looking after you find the first cause.**
> Run it with `{REASON:off}`.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall) — the copy here includes
the tool-call unwrapper and `REASON_MODE` / `TEMP` / `TOP_K` / `MIN_P` / `TOP_P` / `REP_PEN` knobs.
Data: `results/lfm2.5-2.6b-*.json` (six runs: baseline, default+unwrap, off, low, medium, medium+samplers).
