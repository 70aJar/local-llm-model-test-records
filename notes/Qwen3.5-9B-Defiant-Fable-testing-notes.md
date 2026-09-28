# Testing notes — Qwen3.5-9B The Defiant Fable (DavidAU, Q4_K_S)

Companion to `records/Qwen3.5-9B-Defiant-Fable.md`. Harness config, raw observations and the
verification detour that changed the published number. All figures quoted from the run JSONs in
`../results/`.

---

## 1. Harness configuration

| Setting | Value |
|---|---|
| Harness | `harness/full_test_model.py` |
| Engine | LM Studio `:1234` (llama.cpp), OpenAI-compatible `/v1/chat/completions` |
| Model id | `qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp` |
| Quant | **Q4_K_S** 6.1 GB + `mmproj-F32` 1.7 GB |
| Context loaded | 32,768 |
| Residency | sole resident model; no other engine loaded |
| HumanEval | `openai/human-eval` canonical `HumanEval.jsonl.gz`, first 20 |
| Tasks | 5 build prompts |
| Agency | 15 scenarios, 8 tools incl. the `wiki_search` decoy |
| Load time | 4.58 s |

### The two runs

| Run | `TEMP` (HE) | `TASK_TEMP` | `AGENCY_TEMP` | `TOP_P` | `TOP_K` | `MIN_P` | `REP_PEN` |
|---|---|---|---|---|---|---|---|
| A | 1.0 | 1.0 | 1.0 | 0.95 | 20 | 0.0 | 1.0 |
| **B (published)** | **0.6** | 1.0 | 1.0 | 0.95 | 20 | 0.0 | 1.0 |

Run A flattened the card's *general-tasks* sampler across every section. Run B applied the card's
**per-task** guidance — the card specifies a lower temperature for coding than for general tasks.

```bash
# published configuration
MODEL="<id>" LOAD_KEY="<id>" \
TEMP=0.6 TASK_TEMP=1.0 AGENCY_TEMP=1.0 \
TOP_P=0.95 TOP_K=20 MIN_P=0.0 REP_PEN=1.0 HE_N=20 \
python3 harness/full_test_model.py "<id>" "label"
```

### Card's samplers (source of the above)

```
Thinking mode for general tasks:        temperature=1.0, top_p=0.95, top_k=20, min_p=0.0, rep_pen=1.0
Thinking mode for precise coding tasks: temperature=0.6, top_p=0.95, top_k=20   <-- HumanEval
Instruct (non-thinking) mode:           temperature=0.7, top_p=0.80, top_k=20, presence_penalty=1.5
```

---

## 2. Observation — the tool-call format trap (caught BEFORE the battery)

`chat_template.jinja` shows this model emits **XML** tool calls:

```
<tool_call>
<function=example_function_name>
<parameter=example_parameter_1>
value_1
</parameter>
</function>
</tool_call>
```

Our harness reads only `msg["tool_calls"]` and contains **no XML parsing at all**. So the agency and
tool-call sections depend entirely on LM Studio translating Qwen XML → OpenAI JSON.

**A wire probe was run first, as a gate:**

```
tool_calls present : True
  fn=lookup_employee  args={"name":"Sarah Chen"}
```

Translation works, so the battery proceeded. Had it not, the agency score would have been a false
negative of exactly the kind this harness has produced before. **Probe before you score.**

---

## 3. Observation — thinking cannot be turned off

```
enable_thinking=True  -> reasoning_tokens=198  content='42'
enable_thinking=False -> reasoning_tokens=92   content='42'
```

The template supports `enable_thinking: false` (emitting an empty `<think></think>`), and the flag does
reduce reasoning — but it does **not** eliminate it. There is no true thinking-off mode, so no instruct
baseline can be measured for this model through this path.

**Consequence for scoring:** reasoning consumed ~72–85% of completion tokens. A 300-token probe
returned **empty `content`** and looked like a refusal; at 2,000 tokens the same prompt produced a
1,427-character answer. **An empty short answer is a budget artifact, not a refusal — always re-test
with a larger budget before recording a refusal.**

---

## 4. Observation — timings

### HumanEval

| Run | HE | per-problem secs (min / mean / max) | total |
|---|---|---|---|
| A | 20/20 | 4.4 / 17.9 / 176.1 | 359 s |
| B | 19/20 | — | — |

### Tasks

| Task | Run A | Run B |
|---|---|---|
| adherence | 452 ch / 69 s | 484 ch / 106 s |
| expense-tracker | 30,436 ch / 134 s | 32,458 ch / 191 s |
| fake-desktop | 28,452 ch / 134 s | 21,726 ch / 114 s |
| kanban | 41,851 ch / 205 s | 32,682 ch / 169 s |
| reasoning | 2,676 ch / 116 s | 1,510 ch / 62 s |

Run B logged one **`HTTP 400`** on expense-tracker; the harness's retry recovered and the task still
passed. Noted because it appears in the log and should not be mistaken for a failure.

### Throughput

| Run | completion tokens | secs | tok/s |
|---|---|---|---|
| A | 3,529 | 64.1 | 55.1 |
| B | 3,355 | 64.7 | 51.9 |

⚠ Length-confounded — always-on reasoning makes output length vary between runs. Treat ~52–55 tok/s as
a floor.

---

## 5. The verification detour (why the published number is 19, not 20)

Run A returned **20/20**. A perfect score warrants independent checking, so a standalone test re-sampled
`HumanEval/129` five times **using the bare canonical prompt** and got **2/5** — which initially looked
like proof that the 20/20 was inflated by a lucky draw.

**That conclusion was wrong, and the follow-up run corrected it:**

| | Run A (temp 1.0) | Run B (temp 0.6) |
|---|---|---|
| HE items passing in BOTH | **19 of 20** | |
| Item that moved | `HumanEval/10` (A pass → B fail) | |
| `HumanEval/129` | **passed in BOTH runs** | |
| Agency differences | **none — 15/15 in both** | |

`HumanEval/129` is stable **in the harness**, which prepends
`"Complete the following Python function. Provide only the complete function implementation, no
explanations."`. The standalone re-test omitted that prefix. So the 129 variance was an artifact of
**testing the model with a different prompt than the harness uses** — not model instability.

**Lessons, in order of usefulness:**

1. **Compare like with like.** A "spot check" that changes the prompt is not checking the same thing.
2. **A single re-sample is not a stability measurement** — 2/5 on one item also does not generalise.
3. **Run the differential properly** (two full runs, item-by-item) before announcing a cause. The
   correct read was available after run B and not before.
4. The genuine variance is **one item (`HumanEval/10`)**. Published figure = **19/20**, with 20/20
   recorded as an observed sample rather than discarded.

---

## 6. Caveats

- **Vision untested.** Loads as `vlm` with `mmproj`; the template has a full image path. **Claimed, not verified.**
- **MTP not enabled.** The file carries MTP layers; speculative decoding was left off so throughput stays
  comparable across records. MTP speed is a separate measurement.
- **Two samples only.** Not a variance study.
- **Card claims unvalidated.** The card asserts the model beats 7 benchmarks of Qwen3.5-27B / Qwen3.6-35B-A3B
  at 4-bit. This battery is a different instrument and neither confirms nor refutes it.
- **Agency is graded on tool-name selection**, not on generated code, so it is far less
  sampler-sensitive than HumanEval — which is why its perfect score is the more trustworthy number.
