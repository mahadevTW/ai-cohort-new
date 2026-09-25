# Context Engineering — the concepts that matter

The 26 ideas from the notebook that are actually worth knowing, in simple language.

Made for teaching. If you can explain these 26 to a fresher, they have enough to start
working. The notebook has much more detail — come here to revise, go there to run code.

**Teaching order:** Sections 1 and 2 in the first session (~30 min), Section 3 in the second,
Sections 4 and 5 in the third. Do not try to do it all in one go.

---

## Section 1 — How an LLM actually works

**1. The model only predicts the next word**
An LLM takes some text and guesses what word comes next. Then again. Then again.
That is the whole thing. No thinking, no memory, no database lookup.

**2. Tokens are the unit of everything**
The model does not see letters or words. It sees *tokens* — roughly 4 characters each.
You are charged per token and limited per token. So tokens = money and tokens = space.

**3. The model has NO memory**
Every API call is fresh. The model does not remember anything from your last call.
Whatever it needs to know, you must send again. **This one idea explains everything else.**

**4. You send a list of messages, not a string**
Three types: `system` (the rules), `user` (the question), `assistant` (what the model said before).
Think of it like: system = company policy, user = customer request, assistant = your earlier replies.

**5. Same input can give different output**
The model picks words randomly from a probability list. So two identical calls can differ.
Never assume an LLM call is repeatable. Treat it like a flaky external API.

---

## Section 2 — Writing good prompts

**6. Be specific, not polite**
"Explain Redis" gives you a generic blog post. The model had to guess who you are and how much detail you want.
Tell it: who is reading, what to cover, how long, what format. Every guess you remove is one mistake less.

**7. Rules in a prompt are only requests**
If you write "give exactly 5 points", the model will *usually* do it. Not always.
So if your code depends on it, check it in code. Do not trust the prompt.

**8. Structured output is the real fix**
Attach a JSON schema and the reply is *guaranteed* to be valid JSON in that exact shape.
Now the model gives you an object your code can use — no string parsing, no surprises.

**9. Show examples instead of explaining rules**
Some rules are painful to write in words. "When is a complaint high severity vs medium?"
Just show 3 examples. The model picks up the pattern. This works better than a paragraph of rules.

---

## Section 3 — Context engineering (the main idea)

**10. Prompt vs Context — know the difference**
Prompt engineering = *what should I tell the model?*
Context engineering = *what information should the model have before it decides?* The second one matters more.

**11. Bad answer? Check the information first**
When the answer is wrong, most people start rewording the prompt. Usually that is not the problem.
Ask first: **did the model even have that information?** No amount of wording creates missing facts.

**12. You assemble the context, nobody else**
Context = instructions + question + chat history + facts + examples + tool results + rules + output format.
Your code builds all of it. This is just request-building — something you already do every day.

**13. More context is NOT better context**
Extra useless data confuses the model and costs money on every call.
Like giving someone a 50-page document when the answer is in 1 line. They may still find it — or they may not.

**14. Rank your context, do not just cut it**
Mark each piece: critical / important / useful / optional / noise.
When space runs out, drop from the bottom. Never let the cut happen randomly.

**15. Priority is not the same as newest**
Very common bug: "just keep the last 10 messages." But your system instructions are the *oldest* message.
So the window quietly throws away your rules first, and nobody notices.

---

## Section 4 — Managing context as it grows

**16. The context window is a size limit, and output shares it**
Everything you send plus everything the model writes must fit in one window.
If you fill it with input, there is no space left for the answer.

**17. Chat history grows very fast and costs a lot**
The model has no memory, so you resend the whole conversation every single turn.
Turn 20 costs about 20x turn 1. This is the biggest bill in any chat product.

**18. Compress old chat into a summary or a state object**
Do not send 50 old messages. Extract what matters — order id, status, what the user wants — and send that.
Like a case summary instead of the full call recording.

**19. Memory is different from chat history**
Chat history dies when the session ends. Memory survives — "prefers short answers", "is a backend engineer".
Only store things that will still be true next month. Storing today's ETA in memory is a bug waiting to happen.

**20. Tool results are also just context**
The model cannot run anything. It says "call `get_order`", *your code* runs it, and you paste the result back as text.
So a tool result is nothing special. It is more text you chose to add.

**21. Always filter tool results before sending**
A real order API returns phone numbers, payment ids, commission rates — 700 tokens for a "where is my order?" question.
Send only the 3 fields needed. Anything in the context can come out in the answer, and it is in your logs too.

**22. Put important things at the start or the end**
Models pay less attention to the middle of a long context. Same as a long meeting — you remember the start and the end.
So keep instructions at the top and the user's actual question at the bottom.

---

## Section 5 — The part that bites in production

**23. Old and duplicate data quietly breaks things**
If your context has "status: DELAYED" and also an old "status: DELIVERED", the model picks one. Randomly.
Missing data makes the model say "I don't know" — which is safe. Wrong data makes it confidently lie.

**24. Your code should resolve conflicts, not the model**
Decide the rule yourself: what the user just said beats stored memory, fresh data beats old data.
The model does not know which of your systems is more trustworthy. You do.

**25. An agent is just a loop**
Ask model → it wants a tool → run tool → add result to context → ask again. Repeat until it answers.
Nothing magical. But every loop adds more text, so always put a maximum iteration limit.

**26. Judge the context, not only the answer**
Before blaming the model, check: was everything needed present? Was anything stale? Was it too big?
Keep 10 fixed test questions with expected answers. That will help you more than any prompt tweaking.

---

## The 3 lines to remember

1. **The model remembers nothing.** Whatever it knows, you put there in this call.
2. **Wrong answer? Ask "was the information there?" before "was my wording right?"**
3. **Less but correct context beats more context.** Selecting and ordering beats dumping everything.

---

## What was left out

Cut on purpose, because freshers do not need it on day one. It is all still in the notebook:

| Topic | Where |
|---|---|
| Temperature and sampling settings | Part 1.5 |
| Prompt caching (cost optimisation) | Part 15.1 |
| Prompt injection through tool results | Part 16.1 |
| The full 6-stage context pipeline | Part 20 |
| Prompt versioning, retries, timeouts | Part 23 |
