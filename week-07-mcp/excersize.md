# Week 7 — Exercise: move the HR tools into an MCP server

**Ships by the end of this session:** `hr-assistant` v6. The three week-6 tools (`get_leave_balance`, `apply_leave`,
`notify_manager`) live in their own **MCP server**, and the `/agent` page gets its tools from that server.

**In one sentence for a beginner:** *MCP is a standard way for an app to ask another program "what tools do you have?"
and "please run this one". Write the tools once, and any app can use them.*

**Where the code goes.** Your own `hr-assistant` repo. `week7.ipynb` shows the idea; you watch it, you do not build in it.
`hr_mcp_server.py` next to it is a small finished server (about 60 lines). Read it, then write your own version.
The `/agent` page and `/chat` keep working. We move code; we do not change behaviour.

**New package:** `fastmcp`. It is in `requirements.txt`. If your venv is older, run `./.venv/bin/pip install fastmcp`.
One library gives you both the server and the client.

---

## How to teach this (240 min)

| Block | Min | What happens |
|---|---|---|
| Recap + week-6 homework | 15 | Show two failures from the goals table |
| **Concept** | 50 | Why (10) · server and client (10) · what goes over the wire (10) · who decides what (10) · trust (10) |
| **Live build** | 115 | Notebook steps 1-5 (45) · then Parts 1-3 below (70) |
| **Lab** | 45 | Try to break your server |
| Wrap + homework | 15 | Read the homework out loud |

**Say it in this order**

1. **Start from the pain.** *"The voice helpline needs `apply_leave`. How do you give it the tool?"* Copy and paste. Then: *"You fix a bug. Who fixes the copy?"*
2. **The USB idea.** Any device fits any laptop because both follow one standard. MCP does that for tools and AI apps.
3. **Two words:** *server* owns the tools, *client* asks for them. Draw two boxes and an arrow. The model is not in the picture; it never was.
4. **Show the two messages** (notebook step 2): "list your tools", "run this one". That is the whole protocol.
5. **Who decides to use what:** the **model** picks tools, the **app** attaches resources, the **user** picks prompts.
6. **Trust.** A tool description is text that goes into your prompt. Run the "weather" server in step 5.

**Live build.** In the notebook, run and talk; do not type. Spend your time on steps 3, 4 and 5. Step 6 (HTTP) is the first thing to drop.

**If you run behind:** drop Part 3 and make it homework. **Never cut the "ask twice, saved once" check or the human confirm.**

**Four things that always go wrong. Say them before they happen.**

- The server prints something and the client breaks. *The two talk through the same channel `print` uses. Log with `file=sys.stderr`.*
- The server starts and shows nothing. *That is correct. It is waiting for the client.*
- The model "forgets" a tool you just added. *Restart the server. It reads the file once, when it starts.*
- Something is wrong and you do not know whether it is the server or the agent. *Open the server in the Inspector (Part 1). If it works there, the server is fine and the bug is in your client or agent.*

---

## Warm-up (5 min): who decides to use it?

For each, say **model**, **app** or **user**, and so which MCP feature it is (tool, resource, prompt).

1. `get_leave_balance`: live data the model needs in the middle of a chat. *(tool: the model decides)*
2. The leave policy text, attached to every chat about leave. *(resource: the app decides)*
3. A "Request leave" button that fills in a sentence. *(prompt: the user decides)*
4. `apply_leave`. *(tool, and a write, so a human must confirm)*
5. Last quarter's payroll file. *(none of them. Should it be reachable at all?)*

---

## The build

Two new files and two small edits:

```
hr-assistant/
  mcp_server.py     NEW   the three tools, using your tables (mostly moved from agent.py)
  mcp_client.py     NEW   a few lines: connect, list tools, call a tool
  agent.py          EDIT  tools come from the server; the loop and the confirm gate stay the same
  requirements.txt  EDIT  fastmcp (already there)
```

> Builds on week 6. If `agent.py` has no `apply_leave` yet, finish week 6 first. The two tables and the unique
> idempotency keys are the base for everything below.

### Part 1 — The server (25 min)

1. Create `mcp_server.py`. Start from `week-07-mcp/hr_mcp_server.py`, but read and write **your** tables from `db/models.py`
   instead of the reference's Python lists.
2. Put `@mcp.tool` on each of the three functions.
   - the **docstring** is what the model reads. Copy the wording from your week-6 `TOOLS` list
   - the **type hints** (`start_date: str`, `days: int`) become the inputs. You write no schema
   - mark reads with `annotations={"readOnlyHint": True}`
3. **No tool takes an `employee_id`.** Use one fixed employee at the top of the file.
4. **Never `print()`.** Use `print(..., file=sys.stderr)` if you need a log line.
5. End with `if __name__ == "__main__": mcp.run(transport="http", host="127.0.0.1", port=8765)`. You start it once and clients connect to `http://127.0.0.1:8765/mcp`.

Keep the week-6 rules: a failure returns text starting `Error:`, and a write looks for its idempotency key before inserting.

**Check yourself.** Start your server, open it in the Inspector (steps below), and call `apply_leave` twice with the same input.
*Still one row in `leave_requests`?* If not, check the key.

#### Test any MCP server with the Inspector

The **MCP Inspector** is a free tool from the MCP project. It connects to your server as a client and lets you
list and run tools by hand, with no model and no agent. Use it **first**, every time you write or change a server.
It needs Node.js (`npx` downloads it on first run, which can take a minute).

**1. Start the server** in its own terminal and leave it running (from the repo root):

```bash
./.venv/bin/python week-07-mcp/hr_mcp_server.py          # serves http://127.0.0.1:8765/mcp
```

**2. Start the Inspector** in a second terminal:

```bash
npx @modelcontextprotocol/inspector
```

It prints a link (`http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...`) and opens it. Use the full link; the token is part of it.

In the page:

1. Left panel: set **Transport Type** to **Streamable HTTP**, **URL** to `http://127.0.0.1:8765/mcp`. Click **Connect**.
2. Open the **Tools** tab and click **List Tools**. You should see the four tools, each with its description and inputs.
   *This is exactly what a model would see.* If a description is vague here, it is vague to the model too.
3. Click a tool, fill in its inputs, click **Run Tool**. Try these in order:
   - `get_leave_balance`: no inputs. Expect `casual_days_left: 4`.
   - `apply_leave` with a weekday after today (`start_date` = `2027-03-01`, `days` = `1`): expect `submitted`.
   - The same call again. On **your** server (with the week-6 idempotency key) this must not create a second request.
     The reference `hr_mcp_server.py` keeps a plain list and does not check, so it saves twice: a good thing to notice.
   - `apply_leave` with a Saturday: expect text starting `Error:`, not a crash.
   - `notify_manager` with `request_id` = `999`: expect `Error: no leave request 999`.

No browser? Use the command-line mode against the same running server:

```bash
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:8765/mcp --transport http --method tools/list
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:8765/mcp --transport http \
  --method tools/call --tool-name apply_leave --tool-arg start_date=2027-03-01 --tool-arg days=1
```

Every time you edit the server file, stop it (Ctrl+C) and start it again. It reads the file once, when it starts.
This also clears the saved requests, because they live in memory.

**Stdio, the other transport (short note).** Over stdio there is no URL: the client starts the server itself and they talk
through stdin/stdout. It is common for tools that run on your own machine, such as a desktop app. We use HTTP in this
course because a shared server that many apps connect to is how MCP is used for real. If you ever need stdio, run
`hr_mcp_server.py --stdio`, and give the Inspector the start command instead of a URL:
`npx @modelcontextprotocol/inspector ./.venv/bin/python week-07-mcp/hr_mcp_server.py --stdio`.
Over stdio a stray `print()` breaks the connection, which is why servers log to `file=sys.stderr`.

**See it work in an agent.** With the server still running, in the second terminal:

```bash
./.venv/bin/python week-07-mcp/hr_mcp_client.py
```

`hr_mcp_client.py` is about 70 lines: it connects to the URL, lists the tools, and runs a normal agent loop. Read it before Part 2.

### Part 2 — The client (15 min)

In `mcp_client.py`, a few lines:

```python
from fastmcp import Client
hr = Client("http://127.0.0.1:8765/mcp")     # connects to the running server (start mcp_server.py first)

async with hr:
    tools = await hr.list_tools()
    result = await hr.call_tool("get_leave_balance", {})
    print(result.content[0].text)
```

Add the small helper `to_openai(tool)` from the notebook: it turns an MCP tool into the format OpenAI expects.

**Check yourself:** a script that prints the tool names, then the balance.

### Part 3 — The agent, over MCP (30 min)

In `agent.py`, change three things:

1. Get the tool list with `await hr.list_tools()` and convert it with `to_openai`.
2. Work out `WRITES` from the server's labels: every tool **not** marked `read_only_hint`.
3. Run a tool with `await hr.call_tool(name, args, raise_on_error=False)`. The last argument makes an error come back as
   text, as it did in week 6, instead of crashing the loop.

`run_agent` becomes `async def`, so make `POST /agent` `async def` too and `await` it.

**The confirm gate stays in `agent.py`.** Do not move it into the server. In one sentence in your README: *why not?*
(Hint: whose side is the human on?)

**Check yourself. These are the week-6 checks, and they must still pass:**
1. `approved: []` returns `needs_approval`, and `leave_requests` is still empty.
2. `approved: ["apply_leave"]` writes the request, then asks about `notify_manager`.
3. With both, it finishes.
4. Run step 3 twice. Still **one** row and **one** notification.

Then the payoff: add a read-only tool such as `get_manager()` to `mcp_server.py`. **Do not touch `agent.py`.**
Restart and ask *"Who is my manager?"* If the agent uses it, your agent no longer needs to know what tools exist.

**Done for the session when:** the `/agent` page works as before, the tools come from `mcp_server.py`, `agent.py` does not
import them, and the new tool worked without editing the agent.

---

## Lab (45 min): try to break your server

Write one line per answer in your `README.md`.

**1. Bad input (10 min).** With `Client("http://127.0.0.1:8765/mcp")`, call `apply_leave` with a missing input, a word where a number belongs,
and an input the tool never declared. What came back each time? Did the server crash?

**2. The `print` problem (10 min).** Add `print("hello")` to a tool. Call it. What went wrong? Change it to `file=sys.stderr`. Remove it.

**3. Attack a classmate's server (25 min).** Try to:

- apply leave **for someone else** (pass an `employee_id`)
- read **another employee's balance**, or anyone's salary
- **save the same request twice**
- send `notify_manager` for a request id that does not exist, or belongs to someone else
- put an instruction in the `note` ("ignore your rules...") and see where it ends up

For each success, say which rule should have stopped it, and whether that rule lives in the **server** or the **client**.

---

## Definition of done

- [ ] `mcp_server.py` serves the three tools, using your tables
- [ ] No tool takes an `employee_id`; nothing prints to stdout
- [ ] `agent.py` lists tools from the server and works out `WRITES` from the labels
- [ ] The four week-6 checks still pass
- [ ] A tool added to the server alone was used without editing the agent
- [ ] Lab notes in `README.md`
- [ ] Pushed and tagged `week-07-session`

**Homework:** see `assignment.md`. Mandatory, due before week 8, about 3 hours.

---

## The question to leave the room with

A teammate says: *"I found an open-source MCP server for Jira on GitHub and connected it to our agent. It works great."*

If its author were an attacker, which of these would you still trust: **its tool descriptions, its `read_only_hint` labels,
your human confirm, your list of allowed tool names**? Which of those are code that you control?

Next week one agent with all these tools becomes the problem. That is week 8.
