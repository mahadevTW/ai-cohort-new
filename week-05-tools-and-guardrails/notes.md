# Week 5 — Notes: tool calling, live data, and how results enter the prompt

## The one sentence

**A tool result is just another message in the array.** The model never calls anything. It asks;
your code calls; your code pastes the answer in. So a tool result is a week-3 context bucket: it costs
tokens, can be too long, can be stale, and can lie.

## Order of ideas (matches `week5.ipynb`, 8 steps)

0. The problem: ask the time. It has no clock.
1. **`greet(name)`**, in four sub-steps. **1a:** pass only a tool *description* to a bare API call. No function exists yet, and the model still replies with `finish_reason: tool_calls`, empty `content`, and a suggested `greet({"name":"Asha"})`. **The model only suggests. That is the lesson.** **1b:** same tool, ask "12 times 12": it answers directly, so the prompt and descriptions decide. **1c:** now write `greet` and run it yourself with the suggested arguments. **1d:** append the request and a `tool` message, ask again.
2. **`get_current_time()`**: a tool with no arguments, and it fixes step 0. Package the four hand steps into `run_tools()`. Then ask "12 times 12": no `asks for` line. The model chooses whether to use a tool.
3. Two tools, one question. One turn can request several calls.
4. **Exchange rate API**: an API call is just a function. The `[tool]` line is the prompt ingestion.
5. **Public holidays**: shape the result. Lazy (9 fields per holiday) vs trimmed (2 fields): 825 vs 332 prompt tokens, same answer.
6. **API failure**: India returns HTTP 204, the lazy tool crashes with `JSONDecodeError`. Return `Error: ...` as text instead.
7. **Leave balance**: the tool decides what the model sees. Salary never enters the context, so the model cannot leak it.
8. **Poisoned result**: fence the outside text, say what the fence means. Lowers the risk, does not remove it.

Pace: steps 1 to 3 are the whole mechanism. Spend the time there. Steps 4 to 8 are variations.

## Words to say out loud

- "Show me the `tool` message." If you cannot print what entered the prompt, you are guessing.
- "The tool raises → your request dies. The tool returns an error string → the model can react."
- "`fetched_at` is how a stale result becomes visible instead of silently trusted."
- "A fence is a request to the model. A tool that cannot read other people's data is code. Prefer code."

## Message shapes worth drawing on the board

```
{"role": "assistant", "content": null, "tool_calls": [{"id": "call_1", "type": "function",
                                                      "function": {"name": "...", "arguments": "{...}"}}]}
{"role": "tool", "tool_call_id": "call_1", "content": "..."}
```

Every `tool_call` id needs a matching `tool` message, or the next request fails with a 400.
`arguments` is a **string of JSON**, not an object. Parse it yourself, and expect it to be wrong sometimes.

## Questions that always come up

- **"Why not let the model call the API directly?"** It has no network. It produces text. Something has to execute.
- **"Can it call two tools at once?"** Yes. Step 3 shows it (greet and time in one turn). Run every call and answer every `tool_call_id`.
- **"What if it passes bad arguments?"** In the notebook the loop does not catch it, on purpose: students see the crash in step 6, then fix it inside the tool. In the exercise (FR-5) the loop catches everything. The model usually corrects itself when it gets the error as text.
- **"Is the fence enough?"** No. It lowers the rate. The strong defences are structural: read-only tools, identity bound by the server, a human gate on writes (week 6).
- **"Why not return the whole record and let the model pick?"** Tokens, and because anything in context can come out in an answer. `get_leave_balance` returns 3 fields of 6.
- **"Isn't this just RAG?"** RAG is one tool the model can choose to call (`search_policy`). Retrieval stops being automatic.
- **"Should I use LangChain for this?"** Week 7. You will port this loop and it will take minutes.

## Sensitive data: the four lines (10 min)

1. Anything in context can come out in an answer, including to a different employee in a different session.
2. Your logs are a second copy of the data. The trace you added for debugging now contains salaries.
3. Ask what your provider retains, for how long, and where. Legal will ask you; hear it from us first.
4. Redact before the call, not after. The boundary is the API call.

## Advanced RAG, one slide (5 min)

Query rewriting, hybrid (keyword plus vector) search, re-ranking. Name them, say they are this week's
homework, move on. Do not demo.

## Timing

| Block | Min |
|---|---|
| Recap + week-4 homework | 15 |
| Concept | 50 (tool calling 20 · prompt ingestion 15 · sensitive data 10 · advanced RAG 5) |
| Live build | 115 |
| Lab | 45 |
| Wrap + homework | 15 |

If behind: redaction (FR-9) and tests (FR-10) go to homework. Never cut the loop or the identity rule.

## What to carry out of the room

Every question today needed one or two reads. Now ask: *"Apply for 3 days of casual leave next month
and tell my manager."* That is a plan, two writes that must not run twice, and a decision about when
to stop. A five-round `for` loop does not solve that. That is week 6.

## Before delivering

- Run `week5.ipynb` top to bottom the morning of. It calls live APIs (Frankfurter, Nager) and OpenAI,
  so it needs `OPENAI_API_KEY` and network. The saved outputs are from a real run.
- If either API has changed its response shape, Steps 4 and 5 break first. Re-check `rates` and the
  `date`/`name` fields.
- Steps 4, 5 and 6 hit the network on every run. The `SG` calendar changes yearly; the
  "holidays after today" answer depends on the run date.

## Not in the notebook, on purpose

Retries, caching, timeouts, redaction, identity bound by the server, and `search_policy`. They are
the exercise (`excersize.md`). The notebook stays small so the mechanism is visible; the project is
where it gets real.
