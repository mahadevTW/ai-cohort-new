# Week 7 — Assignment

**Due:** 24 hrs before session 8 · PR on your `hr-assistant` repo, tag `week-07` · **~3 hrs**

Builds on the exercise: your `mcp_server.py`, `mcp_client.py`, and an `agent.py` that gets its tools from the server.
Do 1 to 3 in order. Number 4 is optional.

1. **Add a policy tool to your server (45 min).**
   Add your week-4/5 retrieval as a **read-only** tool: `search_policy(question: str)`. It returns the top 3 chunks as a small
   list, with only three fields each (text, document, section).
   - Remove `search_policy` from `agent.py` if you added it last week. The agent must get it **only** from the server.
   - Ask: *"How many casual leaves do I get, and apply for 1 next Monday."* Paste the steps into `README.md`.
   - Also expose the leave policy as a **resource** (`@mcp.resource("policy://leave")`). Two sentences in `README.md`:
     why is this a resource and not another tool, and when would you make it a tool?

2. **Only show the tools you chose (45 min).**
   A server's tool descriptions go straight into your model's prompt (notebook step 5). Defend against that in code.
   - Write `servers.json`: for each server, its **name, the command to start it, and the tool names you allow**.
   - In `mcp_client.py`, hide every tool that is not on the list **before** the model sees it. Do not just ask the model to avoid it.
   - Prove it: add a new tool to your server without adding it to `servers.json`, and show in `README.md` that the agent cannot see it.
   - Stretch: save a short hash of each tool's name + description in `servers.json`, and refuse to connect if it changes later.

3. **Your five goals, now over MCP (60 min).**
   Run your `goals.py` from week 6 (5 goals, each checked against the **database**) through the new agent.
   - Add **two goals** for the new tool: one that needs `search_policy`, and one that needs a policy lookup **and** a write.
   - Paste a table into `README.md`: goal, pass or fail, steps, tokens.
   - Did anything get **worse** after the move? A tool description you shortened while moving it is the usual cause.
     If a goal fails, read its steps and fix the description or the tool, not the check.
   - **Aim for 6 of 7.** At least one goal must be one that should **fail safely**, with nothing written.

4. **Optional: who is calling? (30 min).**
   Your server already runs over HTTP (`mcp.run(transport="http", ...)`). Answer in `README.md`:
   - Over stdio (where a client starts the server itself), the server knew who was calling because only your agent started it. **What does it know over HTTP, where any app can connect?**
   - Two apps use one server: how could the server tell Asha from Karan? Sketch it, do not build it.

### Four sentences (15 min, mandatory)

In `README.md`:

(a) Which line of your **server** stops the same request being saved twice?
(b) Which line of your **client** stops a write before the human says yes?
(c) If another team's server lied about its `read_only_hint`, which of (a) and (b) would still protect you?
(d) One thing about MCP that can still go wrong and that you did not fix.

---

### Self-check before you push

- [ ] `agent.py` does not import any tool function; every tool comes from `list_tools`
- [ ] `mcp_server.py` never prints to stdout (`grep -n "print(" mcp_server.py` shows only `file=sys.stderr`)
- [ ] No tool takes an `employee_id`
- [ ] A tool not in `servers.json` is invisible to the model
- [ ] The goals table is in `README.md`, with 6 of 7 passing (or a written reason why not)
- [ ] The four sentences are written
- [ ] Tagged `week-07`

---

*Next week: LangChain and multi-agent. You will port this agent to LangChain and connect it to the same servers,
so keep `servers.json` and `goals.py` working.*
