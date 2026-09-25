# Context & Prompt Engineering — hands-on lab

A single executable Jupyter notebook that teaches prompt engineering and context engineering
from first principles, using the OpenAI Python SDK directly. Written for an experienced
backend engineer who is new to AI engineering.

| File | What it's for |
|---|---|
| `context_and_prompt_engineering_openai.ipynb` | The lab. 209 cells (90 markdown, 119 code). Run it. |
| `CONCEPTS.md` | The 26 concepts that matter, in simple language, 3 lines each. Built for revising and for teaching freshers. |
| `README.md` | Setup, cost, code style, contents. |

---

## Setup

```bash
cd ~/project/learn-ai

# 1. dependencies (a venv already exists at ./.venv)
pip install openai jupyter

# 2. your API key
export OPENAI_API_KEY="your-key"

# 3. launch
jupyter notebook context_and_prompt_engineering_openai.ipynb
```

To use the venv that is already here:

```bash
source .venv/bin/activate
export OPENAI_API_KEY="your-key"
jupyter notebook context_and_prompt_engineering_openai.ipynb
```

Run the cells **top to bottom** — later cells depend on objects defined earlier.

---

## The model

```python
MODEL = "gpt-4o-mini"
```

One model, everywhere. `gpt-4o-mini` is cheap, fast, and supports every feature the notebook
uses: structured output, tools, and `temperature`. `MODEL` is a single variable — change it in
Part 0 and everything downstream follows.

**Reasoning models are deliberately out of scope.** The `gpt-5` family thinks privately before
answering, which changes some of the rules taught here (`temperature` no longer applies, and you
pay for thinking you never see). Mixing the two would muddy every lesson. That belongs in its own
notebook, once these fundamentals are second nature.

### Cost of a full run

146 API calls, roughly 49,500 input tokens. On `gpt-4o-mini` that is a **few cents**.

Part 0 defines a `PRICING` dict with placeholder per-million-token prices — update it from
<https://openai.com/api/pricing> and the notebook's running cost counter becomes accurate.

---

## How the notebook is structured

Every concept follows the same seven beats:

```text
Concept -> Mental Model -> Flow diagram -> Minimal code
        -> SHOW THE ACTUAL CONTEXT -> Experiment -> Key Takeaways
```

The fifth beat is the point of the whole thing. A helper called `show(messages)` prints the exact
message array being sent, with per-message token counts, so you can always answer *"what did the
model actually receive?"*

### The code style

Deliberately plain, because the concepts are the hard part and the code should not be:

* **Plain dicts, not classes.** A piece of context is `{"kind": ..., "text": ..., "priority": ...}`.
  There are no dataclasses, no `@property`, and only three classes in the whole notebook
  (`Conversation`, `ManagedConversation`, `SupportAssistant`) — each one because it genuinely
  holds state.
* **Readable strings, not constants.** Priority is `"critical"` / `"important"` / `"useful"` /
  `"optional"` / `"noise"`, not an integer you have to look up.
* **Small named functions.** `prioritize()`, `fit_to_budget()`, `filter_stage()` — each does one
  thing and fits on a screen.
* **One `table()` helper** in Part 0 handles every comparison table, so the cells show the
  comparison rather than the formatting code.
* Standard library plus the OpenAI SDK. No frameworks.

There are three helpers to learn in Part 0, and everything else builds on them:
`table()`, `show()`, `llm()`.

### Contents

| Part | Topic |
|---|---|
| 0 | Setup and the `show()` / `llm()` measurement harness |
| 1 | LLM fundamentals: tokens, roles, statelessness, truncation, temperature |
| 2 | Prompt engineering: the ladder, clear instructions, roles, constraints, structured output, few-shot |
| 3 | **Prompt vs context** — the hinge of the notebook |
| 4 | Context fundamentals: the eight buckets and `build_messages()` |
| 5 | Context selection and signal-to-noise |
| 6 | Context prioritization: CRITICAL → NOISE, and budget-aware shedding |
| 7 | Context budget, input and output |
| 8 | Context compression: truncate vs summarize vs extract state |
| 9 | Conversation context and the O(N²) cost of history |
| 10 | Memory: conversation history vs long-term memory |
| 11 | Memory extraction as an idempotent ETL job |
| 12 | Tool results as context — the real wire format |
| 13 | Context filtering: projection and redaction |
| 14 | Lost in the middle, measured on your own model |
| 15 | Context ordering **and prompt caching** |
| 16 | Context pollution **and prompt injection via tool results** |
| 17 | Conflict resolution and precedence policy |
| 18 | Agent context: a hand-written loop, no frameworks |
| 19 | Context growth in agents, and the five levers |
| 20 | The optimization pipeline: collect → filter → rank → compress → order → send |
| 21 | `ContextBuilder` — the reusable architecture |
| 22 | Evaluating context quality, with a golden-set harness |
| 23 | Production mental model, prompt versioning, operational basics |
| 24 | Final project: the AI Support Assistant, using everything |

Ends with the mental-model ladder and a 22-item checklist.

---

## Deliberately out of scope

RAG, embeddings, vector databases, semantic search, document chunking, LangChain, LlamaIndex —
and reasoning models.

Learn RAG next. This notebook is the foundation it sits on: RAG is one more *context selection*
strategy, and everything here about budgets, ordering, filtering, pollution and evaluation
applies to it unchanged.

---

## Validation performed

* The `.ipynb` passes `nbformat.validate()` and re-reads cleanly from disk.
* All 119 code cells parse (`ast.parse`).
* A static pass confirms no cell reads a name that no earlier cell defines.
* All 119 code cells were **executed end-to-end against a stubbed client** (0 failures), proving
  the notebook runs top-to-bottom with no ordering bugs.
* Live API behaviour was not tested — no API key was present in the authoring environment.
