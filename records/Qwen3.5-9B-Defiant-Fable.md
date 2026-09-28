# Model Scorecard — Qwen3.5-9B The Defiant Fable Uncensored Heretic NEO IMATRIX MAX MTP (DavidAU)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-28 |
| **Model** | `DavidAU/Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX-MTP-GGUF` |
| **Base** | `Qwen/Qwen3.5-9B` — 9B, Gated DeltaNet + Gated Attention hybrid, 32 layers, 262,144 native context |
| **Source** | [Hugging Face](https://huggingface.co/DavidAU/Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX-MTP-GGUF) (public) |
| **Quantization** | **Q4_K_S** (6.1 GB) + `mmproj-F32` (1.7 GB) |
| **Engine** | LM Studio `:1234` (llama.cpp backend) |
| **Host** | Apple Silicon M5 Max / 128 GB |
| **Context loaded** | 32,768 (native max 262,144) |
| **Type** | `vlm` — vision-capable; reported `capabilities: ["tool_use"]` |
| **Decensoring** | **Heretic** — trained *after* Heretic'ing. Card claims **6/100 refusals** vs base 100/100, KLD 0.0793 |

## Results

Two full runs. Run A used the card's *general* thinking sampler for every section; Run B applied the
card's **per-task** samplers (the card specifies a different temperature for coding vs general).

| Run | HumanEval | Agency | Tasks | tok/s | Tool-call | Samplers |
|---|---|---|---|---|---|---|
| **A** | 20/20 | **15/15** | **5/5** | 55.1 | ✅ | temp 1.0 everywhere (general) |
| **B — published** | **19/20** | **15/15** | **5/5** | 51.9 | ✅ | HE temp **0.6** (coding) · Tasks/Agency temp 1.0 |

Coverage was **20/20 · 15/15 · 5/5 (100%) in both runs** — nothing truncated, nothing empty, so no
budget artifacts.

**Published figure = Run B (19/20).** Run A's 20/20 is recorded as an observed sample, not the score.

### Stability — what actually varies

Comparing the two runs item by item:

- **19 of 20 HumanEval problems pass in BOTH runs.** Only **`HumanEval/10`** moved (pass → fail).
- **Agency is identical in both runs — all 15 scenarios, zero differences.**
- Tasks 5/5 in both, all with working code.

So this model's variance is confined to roughly **one HumanEval item**; its agency behaviour is
reproducible.

### Agency breakdown — 15/15 (perfect)

```
dept_lookup            PASS  ['lookup_employee']
list_active_eng        PASS  ['search_directory']
count_eng              PASS  ['search_directory']
list_support_platform  PASS  ['search_directory','search_directory']
book_room_b            PASS  ['book_room']          <-- solves the booking mutation
book_room_a            PASS  ['book_room']          <-- solves the booking mutation
check_room_b           PASS  ['check_availability']
ticket_manager         PASS  ['lookup_employee']
ticket_support_lead    PASS  ['search_directory']
ticket_platform        PASS  ['search_directory']
convert_eur_usd        PASS  ['convert_currency']
convert_usd_jpy        PASS  ['convert_currency']
restraint_thanks       PASS  []                     <-- correctly abstains
restraint_weather      PASS  []                     <-- correctly abstains, no decoy call
focus_team             PASS  ['lookup_employee']
```

Two results here are notable against our fleet baseline:

1. **Both `book_room_a` and `book_room_b` pass.** Every other model we have tested solves at most one
   of this pair — the family trait is to call `check_availability` and stop without ever issuing the
   booking mutation. This model solves both, in both runs.
2. **`ticket_support_lead` passes.** This scenario failed in *all six* prior runs of the previous model
   tested, and is a stable limitation there.
3. **`restraint_weather` correctly makes no call.** The scenario has no valid tool; the correct
   behaviour is to abstain rather than reach for the `wiki_search` decoy. Some sampler configurations in
   our other tests over-call here — this model does not.

## Observations (harness-level, this model)

- **Thinking is effectively always on.** `chat_template_kwargs: {enable_thinking: false}` **reduces**
  reasoning but does not eliminate it (measured 198 → 92 reasoning tokens, never 0). There is no true
  thinking-off mode, so no instruct baseline exists for this model.
- **Reasoning dominates the token budget.** In the default mode ~72–85% of completion tokens are
  reasoning (e.g. 829 of 1,153 on a creative prompt). **A short `max_tokens` returns empty `content`** —
  this is a budget artifact, not a refusal. Our first 300-token probe looked like a refusal and was not.
- **Tool calls are XML in the chat template, but served as OpenAI JSON.** The template specifies
  `<tool_call><function=NAME><parameter=X>value</parameter></function></tool_call>`; our harness reads
  only `msg["tool_calls"]`. **Verified on the wire that LM Studio translates this correctly** before the
  battery was allowed to run — `lookup_employee({"name":"Sarah Chen"})` came back as a clean tool call.
  Without that gate check the agency score would have been a false negative.
- **Code answers arrive as markdown blocks**, not tool-call wrappers — unlike some agent-RL models in
  this class. The standard code extractor works unmodified.
- **MTP variant.** The file carries `language_model.mtp.*` layers. Speculative MTP decoding was **not**
  enabled for these runs, so the throughput figures stay comparable to our other records. MTP speed is a
  separate measurement.

## Caveats

- **HumanEval has one borderline item.** ±1 on HE is within the model's real variance; do not treat 20/20
  and 19/20 as meaningfully different capabilities. The agency result is the trustworthy one.
- **Throughput is length-confounded** — measured on a fixed prompt, but this model's always-on reasoning
  makes its output length vary. Treat ~52–55 tok/s as a floor, not an engine rating.
- **Vision claimed but not scored.** The model loads as `vlm` with `mmproj`, and the vision path exists in
  the template — but this battery does not test images. **Untested, not verified.**
- **The card's headline claims were not validated.** It asserts this model exceeds 7 benchmarks of
  Qwen3.5-27B / Qwen3.6-35B-A3B *at 9B in 4-bit*. Our battery is a different instrument; this scorecard
  neither confirms nor refutes that claim.
- **Two samples.** Run A/B only. Not a variance study.

## Verdict

> **The strongest small model in our records so far, and the first to score a perfect agency result.**
> At 8.4 GB it solves **15/15 tool-calling scenarios** — including both halves of the room-booking pair
> that defeats our 27B and 35B-A3B models — and **19–20/20 HumanEval** with clean tool-call compliance.
> Both runs were fully answered, and the agency behaviour reproduced exactly across two different sampler
> configurations, so this is not a lucky sample.
>
> The instruction to take from it is about *method*, not the model: reading `chat_template.jinja` first
> revealed XML tool calls that our harness cannot parse, and a 30-second wire probe proved LM Studio
> translates them. Skipping that step would have produced a confident, wrong agency score — the same
> failure that previously made a good 2.6B model look like it could not write code at all.

---
Harness: `harness/full_test_model.py`. Data: `results/A1-qwen3.5-9b-defiant-fable-q4ks-thinking.json` (temp 1.0)
and `results/A1-qwen3.5-9b-defiant-fable-CORRECTED-cardsamplers.json` (per-task samplers, published).

**Testing notes:** [`notes/Qwen3.5-9B-Defiant-Fable-testing-notes.md`](../notes/Qwen3.5-9B-Defiant-Fable-testing-notes.md)
