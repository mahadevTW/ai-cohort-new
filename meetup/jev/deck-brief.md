# Deck Brief — "Jev & System One AI: When software needs decisions, not text"

Build a 21-slide presentation from this brief. Everything outside a "Speaker notes" block is
content or an instruction for the slides. Speaker notes go in the notes field, not on the slide.

## 1. Context

| | |
| --- | --- |
| Event | Meetup talk, 90 minutes total: about 74 min of slides and live demos, the rest Q&A |
| Audience | Software engineers and IT professionals. Some students with little or no LLM knowledge |
| Tone | Honest, technical, calm. A meetup talk, not a vendor pitch |
| Presenter | Rebind Rise (logo on the title slide only) |
| Core message | LLM generates language. Jev produces decisions. Your code controls what happens |
| Honest-framing line | Jev is not more accurate than a frontier LLM. It is cheap enough to run on every request, and calibrated enough to know when to hand off |

## 2. Brand and style rules

### Palette

| Role | Hex | Use |
| --- | --- | --- |
| Rebind Indigo | `#364E96` | Headings, LLM elements, primary emphasis |
| Deep Indigo | `#293873` | Borders on indigo shapes |
| Rise Cyan | `#12A2DE` | Jev elements, accents, shapes |
| Sky Cyan | `#64D1E5` | Accents on dark slides |
| Midnight | `#0F1B3D` | Body text, dark slide background, "your code" elements |
| Ocean | `#0B7BAA` | Cyan-family text on light slides |
| Slate | `#5B6785` | Captions, sources, slide numbers |
| Mist | `#F4F7FC` | Default slide background |
| Tint | `#E6ECF8` | Cards, table header rows, code backing on light slides |
| White | `#FFFFFF` | Cards, text on indigo or midnight |
| Caution | `#B45309` | Warnings, human/escalation |
| Success | `#15803D` | "Good for" |
| Danger | `#B3261E` | "Breaks on", "do not" |

Gradient: `linear-gradient(90deg, #364E96, #12A2DE)`. Use it only on slide 1 and on the
full-screen statement on slide 15.

### Fixed color meaning (never swap between slides)

| Concept | Color |
| --- | --- |
| LLM (generates, "System Two") | Rebind Indigo `#364E96` |
| Jev (decides, "System One") | Rise Cyan `#12A2DE` |
| Your code (controls) | Midnight `#0F1B3D` |
| Human / escalation | Caution `#B45309` |

### Contrast rules (important)

* **Never put white text on Rise Cyan, and never put Rise Cyan text on white.** Both are 2.9:1
  and unreadable from the back of a room. Put Midnight text inside cyan shapes. Use Ocean
  for cyan-colored text on light backgrounds.
* Body text: Midnight on Mist or White. Headings: Indigo.
* On dark slides: White text, Sky Cyan for the one key phrase.

### Templates

| Template | Background | Text | Used on slides |
| --- | --- | --- | --- |
| Title | Gradient | White | 1 |
| Standard | Mist `#F4F7FC` | Midnight body, Indigo headings | Most |
| Statement | Midnight `#0F1B3D` | White, one Sky Cyan key phrase, centered | 2 (reveal), 15, 20 |
| Demo / code | Midnight `#0F1B3D` | Code in White, keywords Sky Cyan | 3, 9, 16 |

### Typography

* Titles: Inter or Poppins Semibold, 40-44pt
* Body: Inter Regular, 24-28pt, **never below 22pt**
* Tables: Inter, 20pt minimum. If a table does not fit at 20pt, drop columns or rows
* Code: JetBrains Mono or Fira Code, 20-22pt, at most 12 lines
* Captions and sources: Inter, 16pt, Slate

### Layout

* One idea per slide. At most 6 lines of text, or one diagram, or one code block
* Left-align text. Center only on Statement slides
* Margins at least 5% of the slide width
* **Do not put the Rebind Rise logo or tagline on any slide except slide 1.**
  No logo and no tagline in headers, footers or corners elsewhere
* Footer: slide number only, bottom-left, in Slate
* Use no more than one accent color per slide besides the fixed LLM/Jev/Code colors
* Diagrams are vector shapes, using the color meanings above. Do not use screenshots of
  third-party material

### Claim chips

Every number that comes from a vendor or a test gets a small chip next to it. Chips make the
source visible and work in greyscale because they carry a text label.

| Chip text | Fill | Text color |
| --- | --- | --- |
| VENDOR CLAIM | `#FDF0DD` | `#92400E` |
| OUR MEASUREMENT | `#E6ECF8` | `#364E96` |
| INDEPENDENT | `#DDF3E4` | `#166534` |
| CONCEPTUAL | `#E6F6FD` | `#0F1B3D` |

---

## 3. Slides

### Slide 1 — Title (Title template)

* **Title:** Jev & System One AI
* **Subtitle:** When software needs decisions, not text
* **Visual:** Two columns with an arrow down each: `LLM → Generate → Text` and
  `Jev → Decide → Typed result`. The LLM column is indigo, the Jev column is cyan.
* **Logo:** Rebind Rise logo (`main_logo.png`) on a white rounded panel, small, lower area.
  This is the only slide with the logo.

Speaker notes: Do not start with product details. Start with the question: "When your
software calls an AI, does it always need an answer written in English?"

---

### Slide 2 — What does our software actually need?

* **Title:** What does our software actually need?
* **Left:** A quoted customer message in a card:
  "My card was charged twice for the same order and I've been waiting for three days. Please refund me."
* **Right (revealed on click, code styling):**
  ```json
  {
    "intent": "refund",
    "urgency": "high",
    "needs_human": true
  }
  ```
* **Bottom, large (Statement style):** Why run a text-generation engine when the application only needs a decision?

Speaker notes: Ask the room first what the software needs. They will say intent, urgency,
fraud, human review. Then reveal the JSON. Transition: "To answer that, we need a few minutes
on what an LLM actually does."

---

### Slide 3 — What an LLM actually does (Demo / code template)

* **Title:** One token at a time
* **Body:** Placeholder area for a live terminal streaming a model response, token by token.
  Do not fill it with an image.
* **Below, small diagram:** `Input → Tokens → Transformer → token → token → token → text`, with an
  arrow looping from each output token back to the transformer, labelled "each token feeds the next"
* **Caption:** Token = a chunk of text, roughly three quarters of a word

Speaker notes: Stream a response live for 30 seconds. Say: "Everything you just watched is one
model predicting one token at a time. Nothing about that changes when you ask for JSON."
No transformer math. Define inference, latency and autoregressive in one phrase each as they come up.

---

### Slide 4 — Structured output is not a decision model

* **Title:** Structured output is not a decision model
* **Diagram, one row:** `LLM → generate tokens → JSON → schema validation → application`
* **Two short points:**
  * Constraining the format fixes parse failures and schema errors
  * It does not change what the engine is: a general-purpose text generator doing a narrow decision
* **Bottom line:** "Is this customer requesting a refund?" The LLM path is understand, reason,
  generate, format, return. Software needs: YES

Speaker notes: Transition: "That gap is the whole topic of this talk."

---

### Slide 5 — Generative AI vs Decision AI

* **Title:** Two different jobs
* **Diagram (tree):**
  ```mermaid
  flowchart TD
      APP["AI APPLICATION"] --> GEN["GENERATIVE AI<br/>GPT / Claude / etc.<br/>generates things"]
      APP --> DEC["DECISION AI<br/>Jev<br/>evaluates things"]
      GEN --> T["text"]
      GEN --> CO["code"]
      GEN --> RE["reasoning"]
      DEC --> CH["choice"]
      DEC --> SC["score"]
      DEC --> NO["noul"]
      T & CO & RE --> HA["Humans / agents"]
      CH & SC & NO --> SW["Software"]
      classDef llm fill:#364E96,stroke:#293873,color:#FFFFFF;
      classDef jev fill:#12A2DE,stroke:#0B7BAA,color:#0F1B3D;
      class GEN,T,CO,RE llm;
      class DEC,CH,SC,NO jev;
  ```
* **Caption:** LLMs generate tokens. Jev evaluates questions.

Speaker notes: One line on alternatives, then move on: "Jev is one implementation of this idea.
There are others: traditional classifiers, LLMs with structured outputs, OpenAI's Decisions API,
Databricks ai_decide, self-hosted decision models like AWS's Strands Decider. We are not comparing
them today. What matters is that decision-oriented AI is a category, not one product."

---

### Slide 6 — System One and System Two

* **Title:** Fast and slow
* **Source line:** Daniel Kahneman, *Thinking, Fast and Slow*
* **Two columns:**

  | System One (Jev) | System Two (LLM) |
  | --- | --- |
  | Fast, automatic | Slow, deliberate |
  | Effortless | Effortful |
  | Snap judgement: a face is friendly | Working it out: 17 × 24 |
  | Fast and systematically biased | Reasons step by step |

* **Bottom line:** Jev does not replace System Two. It handles a different kind of work.
* **Diagram option:** simple line drawing, a smiling face on the left, "17 × 24" on the right.

Speaker notes: System One is the fast, intuitive one. Make the caveat on purpose: Kahneman's System
One is fast and also biased. That is why this talk is about confidence thresholds. A fast judgement
is useful precisely because you know when not to trust it. Optional one-liner (skip if short on time):
@ShenSeanChen on X, "intuition is compressed reasoning" — a speculative direction, not what Jev does today.

---

### Slide 7 — What is Jev?

* **Title:** What is Jev?
* **Definition, large:** Unstructured state in. Typed, calibrated decisions out.
* **Three facts:**
  * Released by TypeSafe AI, September 2026. The first "System One" model
  * Transformer-based, but not an LLM: no token-by-token generation, no prose
  * Text input only (strings, JSON, arrays of text)
* **Diagram:**
  ```mermaid
  flowchart LR
      S["State<br/>(unstructured text)"] --> Q1["Q1 → typed answer + probabilities"]
      S --> Q2["Q2 → typed answer + probabilities"]
      S --> Q3["Q3 → typed answer + probabilities"]
      S --> Q4["Q4 → typed answer + probabilities"]
      Q1 & Q2 & Q3 & Q4 --> C["YOUR CODE"]
      C --> B["Business action"]
      classDef jev fill:#12A2DE,stroke:#0B7BAA,color:#0F1B3D;
      classDef code fill:#0F1B3D,stroke:#0F1B3D,color:#FFFFFF;
      class Q1,Q2,Q3,Q4 jev;
      class C code;
  ```
* **Caption:** Questions run in parallel and in isolation against the same state

Speaker notes: Say "it does not generate tokens one at a time", not "it is not a transformer".
Do not describe the internals beyond "parallel evaluation". They are not public.

---

### Slide 8 — Three primitives: Choice, Score, Noul

* **Title:** You ask in three shapes
* **Table:**

  | Primitive | Question shape | Returns | Example |
  | --- | --- | --- | --- |
  | **Choice** | Pick 1 of up to 255 | choice, probabilities, confidence | Which team owns this? |
  | **Score** | Position on a rubric you define | score, probabilities, confidence | How urgent is this? |
  | **Noul** | Probability a statement is true | one probability from 0 to 1, **no confidence field** | Is this fraud? |

* **Three one-line tips under the table:**
  * Choice: `criteria` is a dict of option to definition. The definitions are where accuracy comes from
  * Score: you define the ladder, it tells you which rung and how sure it is
  * Noul: write a statement, not a question: "This message conveys urgency"

Speaker notes: "Noul" is TypeSafe's coined word for a yes/no probability. Pronounce it, define it
once, move on. Flag the asymmetry now: Noul has no separate confidence field, and distance from 0.5
is the confidence signal. Do not describe Score as "a number out of 10".

---

### Slide 9 — Live demo 1: one question (Demo / code template)

* **Title:** One question, one response
* **Code:**
  ```python
  from typesafe_sdk import Noul, TypeSafeClient

  client = TypeSafeClient()

  r = client.system_one(
      state="My card was charged twice and I've been waiting three days. Refund me.",
      model="jev-latest",
      questions={
          "is_refund_request": Noul(
              instructions="The customer is asking for a charge to be reversed",
          ),
      },
  )

  print(r.answers["is_refund_request"].noul)
  print(r.usage)
  ```
* **Right side, three callouts:** Under a second. A float, not a sentence. Output is not billed.

Speaker notes: About 3 minutes. Run it live. Then: "That's the whole idea. The rest of this talk
is why that matters and when it fails." If the API fails, play the recorded run.

---

### Slide 10 — Where the calibration comes from

* **Title:** How Jev is trained differently
* **Diagram:**
  ```mermaid
  flowchart TD
      P1["Phase 1 · Pretraining<br/>the world's text: docs, books, code, chat"] --> P2["Phase 2 · RLHF<br/>Reinforcement Learning from Human Feedback<br/>humans rate the answers"]
      P2 --> L["Chat LLM<br/>rewarded for answers people prefer"]
      P1 -.-> R["Phase 2 · RLCD<br/>Reinforcement Learning for Calibrated Decisions<br/>probabilities scored against real outcomes"]
      R --> J["Jev<br/>rewarded for honest uncertainty"]
      classDef llm fill:#364E96,stroke:#293873,color:#FFFFFF;
      classDef jev fill:#12A2DE,stroke:#0B7BAA,color:#0F1B3D;
      class P2,L llm;
      class R,J jev;
  ```
* **Quote, in a card, with a source line (TypeSafe documentation):**
  "Calibration is measured across groups of predictions; it does not guarantee that an
  individual answer is correct."

Speaker notes: Two minutes, conceptual only. "A chat model is rewarded for answers people like. Jev
is rewarded for being right about how sure it is. That is what makes the confidence number worth
gating on." TypeSafe has not published the full training recipe, so say "trained for calibrated
decisions" and stop there. No reward-model or RL math.

---

### Slide 11 — Probability is not confidence

* **Title:** The decision says what. Confidence says how much autonomy.
* **Left, example:**
  ```text
  Billing     0.60
  Technical   0.25
  Account     0.15
  → selected: Billing
  ```
  with the question underneath: "Should our software automatically act on this?"
  Answer: not necessarily. This distribution is flat.
* **Right, threshold policy table:**

  | Action type | Threshold |
  | --- | --- |
  | Low-risk, reversible | Lower |
  | High-risk | Higher |
  | Destructive or irreversible | Human confirmation, always |

* **Diagram (small):** Jev gives Decision and Confidence, which flow into CODE, which splits into
  Automate, Verify, Human. Jev cyan, code midnight, Human caution amber.

Speaker notes: Confidence captures the shape of the distribution, not just the winner. Never say
"Jev is 90% confident, so we are safe". Say "confidence is a signal our software uses to decide how
much autonomy to grant". Thresholds are a risk decision, not a model setting.

---

### Slide 12 — Two cost models

* **Title:** Where the cost comes from
* **Two columns:**
  * **LLM:** input tokens + output tokens (usually the expensive half) × calls × retries.
    Even a one-word decision needs a full generation pass
  * **Jev:** $0.042 per 1M input tokens. Output not metered `VENDOR CLAIM`
* **Footnote chip:** Early-access pricing, subject to change. Verify before the session.
* **Bottom line:** For decision-heavy work the expensive half of the bill, generated output, is not there.

Speaker notes: Do not say "Jev is always 400 times cheaper". The mechanism is that Jev does not
generate output tokens autoregressively. Fill in the LLM-side price from today's published prices
if you want a comparison number, and label it `OUR MEASUREMENT`.

---

### Slide 13 — Batching and latency

* **Title:** Same state, many decisions, one request
* **Left diagram:** Serial LLM: Ticket → LLM → intent, → LLM → urgency, → LLM → fraud
  (3 calls, 3 generations, 3 round trips). Right: Ticket → Jev (one request) → intent, urgency, fraud
* **Two big numbers with chips:**
  * 13 questions in one request: $0.000497, 12.2× cheaper and 10× faster than 13 separate calls `VENDOR CLAIM`
  * End to end: 70 to 500 ms, workload dependent `VENDOR CLAIM`
* **Placeholder box:** "Our measured p50 / p95: ___ ms" `OUR MEASUREMENT` (the presenter fills this in)

Speaker notes: Do not say "always under 100 ms". Measure your own p50 and p95 during prep and put
them in the placeholder. Your own number is more persuasive than a vendor range.

---

### Slide 14 — But is it actually right?

* **Title:** Accuracy: what the evidence says
* **Table:**

  | Test | Jev | Frontier LLM | Source |
  | --- | --- | --- | --- |
  | TypeSafe's own 4-workflow benchmark | about 68% agreement | near mid-tier LLMs | `VENDOR CLAIM` |
  | Phishing detection, 2,000 emails | 62.6% | Claude Haiku 4.5: 81.3% | `INDEPENDENT` |
  | 77-intent banking routing | 78.3% | Opus 5.5: 85.7%, GPT-6 Sol: 85.3% | `INDEPENDENT` |

* **Callout 1:** The vendor benchmark's "correct answer" is the average of two other models'
  answers (GPT-6 Astra and Fable 5.1). It measures agreement, not truth
* **Callout 2 (success color):** Calibration holds: at confidence 0.9 or higher, Jev was right 94 to 96%
  of the time on classification `INDEPENDENT`
* **Bottom line:** On raw accuracy, a frontier LLM wins. That is not the pitch.

Speaker notes: The moment you say "much cheaper", every engineer thinks "at what accuracy?".
Answer it first. On the phishing task calibration error was 0.154 for Jev versus 0.097 for Haiku.
Independent testers found accuracy swings with prompt wording, so budget time for question design and evals.

---

### Slide 15 — So what is the pitch? (Statement template, gradient accent)

* **Full-screen statement, centered:**
  **Jev is not more accurate than a frontier LLM.**
  It is cheap enough to run on every request, and calibrated enough to know when to hand off.
* **Below, small flow:** 1,000,000 requests → Jev → confidence ≥ 0.9: auto-handle (about 94 to 96% correct)
  / confidence < 0.9: escalate to an LLM or a human

Speaker notes: This is the engineering insight. You use a cheap calibrated model as a first-pass
filter so the expensive model only sees the hard cases. Accuracy at high confidence matters more than
accuracy overall. Cost sketch: about 17 dollars of input for a million requests. Label that as
`OUR MEASUREMENT` and compute it for your own token counts.

---

### Slide 16 — Live demo 2: support-ticket router (Demo / code template)

* **Title:** Support-ticket router
* **Left, the three questions as a card:** `intent` is a Choice. `urgency` is a Score.
  `needs_human` is a Noul
* **Right, code (trimmed):**
  ```python
  response = client.system_one(
      state=ticket,
      model="jev-1.13.0",
      questions={
          "intent":      Choice(instructions="Which team should handle this ticket",
                               criteria={"billing": "...", "technical": "...", "account": "..."}),
          "urgency":     Score(instructions="How time-critical is this request",
                               criteria=["Routine", "Time-sensitive", "Critical"]),
          "needs_human": Noul(instructions="This request requires immediate human intervention"),
      },
  )
  a = response.answers

  if a["needs_human"].noul >= 0.85:
      route_to_human(ticket)
  elif a["intent"].confidence >= 0.85:
      auto_route(ticket, a["intent"].choice)
  elif a["intent"].confidence >= 0.60:
      auto_route_with_audit_flag(ticket, a["intent"].choice)
  else:
      escalate_to_llm(ticket)
  ```
* **Bottom line (large):** Jev does not own the business workflow. Your code does.

Speaker notes: About 11 minutes, live. Flow: show the ticket, ask the room what the app needs, send one
request with three questions, show the answers and confidence, apply plain Python branching, add confidence
gating, show the action. Close by printing the wall-clock time and token usage: three decisions, one
request, sub-second, a fraction of a cent. Note that Noul has no confidence field, so the gating code uses
its probability directly. Run an offline replay if the network fails.

---

### Slide 17 — Pattern: routing

* **Title:** Route before you spend
* **Diagram:**
  ```mermaid
  flowchart TD
      REQ["Incoming request"] --> J["Jev<br/>What is this? How hard is it?"]
      J -->|simple| CODE["Plain code path<br/>no LLM call"]
      J -->|moderate| SM["Small / medium LLM"]
      J -->|complex| FR["Frontier LLM"]
      J -->|low confidence| ESC["Escalate: bigger LLM or a human"]
      classDef llm fill:#364E96,stroke:#293873,color:#FFFFFF;
      classDef jev fill:#12A2DE,stroke:#0B7BAA,color:#0F1B3D;
      classDef code fill:#0F1B3D,stroke:#0F1B3D,color:#FFFFFF;
      classDef human fill:#FDF0DD,stroke:#B45309,color:#92400E;
      class J jev;
      class SM,FR llm;
      class CODE code;
      class ESC human;
  ```
* **Two use cases, one line each:**
  * Intent routing: customer support, IT tickets, incident and document routing
  * Model routing: if Jev misroutes, the cost is a suboptimal route, not a wrong answer. The chosen LLM still produces the output

Speaker notes: Model routing is the most defensible pattern because it is the slide 15 argument made
structural. Lower average cost and latency, and better use of model tiers. Optional worked example, labelled
`OUR MEASUREMENT`: 1,000,000 tickets a month at about 400 input tokens is 400M tokens, about $16.80 a month on
Jev input. Compute the LLM side from today's prices before presenting any ratio.

---

### Slide 18 — Pattern: risk and policy triage

* **Title:** Jev supplies the signal. Your rules decide.
* **Diagram:** Customer / order / event → Jev → risk signal + confidence → deterministic rules engine →
  allow / review / block. Jev cyan, rules engine midnight, review in amber
* **Fits:** fraud, abuse, content policy, trust and safety, transaction review, compliance triage
* **Warning callout (caution color):** Putting Jev in front of an LLM agent's tool calls is risk reduction,
  not a security boundary. Jev can be manipulated by adversarial text inside the state you give it.
  Use it to catch mistakes. Use deterministic permissions to stop attacks

Speaker notes: Same point as slide 16: your code stays authoritative.

---

### Slide 19 — Where it breaks

* **Title:** Know the limits
* **Left, "Good for" (success color):** classification and routing; scoring against a rubric; yes/no
  semantic judgements; risk and triage signals; high-volume, latency-sensitive decisions; first-pass filtering
* **Right, "Breaks on" (danger color):** arithmetic and counting; date comparisons; multi-hop reasoning;
  double negatives; noisy or irrelevant state; adversarial text in the state; long-form generation, chat, code
* **Highlighted callout:** No consistency guarantee between related questions in one request. You can get a
  confident yes to both "is this a refund request?" and "is this a technical issue?". If options are mutually
  exclusive, your code must enforce it
* **Bottom row, specs in small type:** text only · 64k token context · up to 255 choices ·
  1,200 requests/min · **early access, closed weights, no self-hosting**

Speaker notes: Say the last row out loud. Early access, closed weights, a single vendor and unproven
pricing durability are a real procurement risk, and the room will respect you for naming it. If someone
raises "zero hallucinations": it means the schema is always valid, not that the answer is correct.
Use the smallest AI primitive that solves the problem, and own the invariants yourself.

---

### Slide 20 — The takeaway (Statement template)

* **Three lines, large, stacked:**
  **LLM = Generate** (indigo)
  **Jev = Decide** (cyan)
  **Code = Control** (white on midnight)
* **Below, decision guide:**

  | What does my software need? | Use |
  | --- | --- |
  | Calculate tax | Code |
  | Is this fraudulent? | Jev, with a human on low confidence |
  | Which queue does this go to? | Jev |
  | Write the customer's reply | LLM |
  | Write code | LLM |

* **Final line, small:** The future of AI engineering is software combining the right intelligence
  primitive for each job, and owning the decisions that matter.

---

### Slide 21 — Resources

* **Title:** Take it with you
* **List (monospace):**
  ```text
  Docs      docs.typesafe.ai
  Endpoint  POST https://api.typesafe.ai/v1/systemone
  Python    pip install typesafe-sdk
  JS/TS     npm install @typesafe-ai/sdk
  OpenRouter  openrouter.ai/docs/guides/community/jev
  Access    early access, waitlist
  ```
* **Placeholders:** QR code to the demo repo (large, right side) · slides URL · contact
* Leave this slide up through Q&A

---

## 4. Backup slides (after slide 21, hidden, not presented)

Build these but mark them hidden. They answer likely Q&A.

| Backup | Content |
| --- | --- |
| B1 — Terms | Table: Token, LLM, Autoregressive, Inference, Structured output, Latency, Confidence, each with a plain one-line meaning |
| B2 — Full specs card | Endpoint, SDKs, model `jev-latest` (currently `jev-1.13.0`), 64k context, 1,200 requests/min and 250k tokens/sec, 255 choice options, text only, English most accurate, pricing, latency, availability |
| B3 — Request and response | The full Python request from slide 16, a short curl equivalent, and the response shape: `answers[id].choice / .score / .noul`, `.probabilities`, `.confidence`, `usage` |
| B4 — Confidence gating code | The full gating code, including `human_certainty = abs(noul - 0.5) * 2` for Noul |
| B5 — LLM vs Jev comparison | Table: purpose, output, how produced, billing, answer space, multiple decisions, confidence signal, accuracy ceiling, best at |
| B6 — Q&A answers | Seven rows: more accurate than GPT/Claude? Self-host? Pricing change? Why not a BERT classifier? Why not structured outputs? How to evaluate? Does it hallucinate? |

## 5. Do not include on any slide

* Transformer math, attention equations, training details beyond slide 10
* Claims like "always 400× cheaper" or "always under 100 ms"
* The phrase "Jev is 90% confident, so we're safe"
* A competitor-by-competitor comparison
* The Rebind Rise logo or tagline anywhere except slide 1
* Any text smaller than 16pt, or body text smaller than 22pt
