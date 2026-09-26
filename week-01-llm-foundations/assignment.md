# Week 1 — Assignment

**Due:** 24 hrs before session 2 · PR on your `hr-assistant` repo, tag `week-01` · **~2 hrs** · every change is an edit to the service you already built.

1. Add `samples: int = 1` to `POST /chat` — it sends the same message array that many times and returns every reply plus `unique_replies`.
2. Call it with `samples=10` at `temperature=0`, then at `temperature=1.2`. Put both `unique_replies` counts in `docs/week1.md`. **Was temperature 0 actually deterministic?**
3. Send a `temperature`. Paste what came back, error text included. **Why does this model not have the knob?**
> Add /usage api it should be usage data till now along with history of usage
5. **Give it a face.** Serve the UI from your own service with `Jinja2Templates` — one `templates/chat.html`, plain CSS and vanilla JS, no CDN and no framework. `GET /` renders it, the send button calls your `/chat`, replies land in the thread, and a corner badge shows tokens and cost for the last turn plus the running total for the page. Screenshot it in your PR.
6. Your page keeps the conversation in a backend array and sends it back as `history` on every turn. Refresh the tab.
7. Change nothing else: no database, no history assembled on the server. Those are weeks 3 and 2, and fixing them now removes the lesson.

Bring to session 2: your chat page open, and the number that surprised you.
