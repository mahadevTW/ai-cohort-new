"""The simplest MCP agent: it connects to the HR server over HTTP and lets the model call its tools in a loop.

1. In one terminal (repo root, venv activated), start the server and leave it running:
       python week-07-mcp/hr_mcp_server.py
2. In another terminal (repo root, venv activated), run:
       python week-07-mcp/hr_mcp_client.py
       python week-07-mcp/hr_mcp_client.py "How many casual leave days do I have left?"
3. Watch the server terminal: it logs every tool call and what it has saved so far.

fastmcp's Client is async. The two helpers below wrap it with asyncio.run, so the rest of the file is plain sync code.
"""

import asyncio
import json
import sys

from dotenv import load_dotenv
from fastmcp import Client
from openai import OpenAI

load_dotenv()
llm = OpenAI()
MODEL = "gpt-4o-mini"
URL = "http://127.0.0.1:8765/mcp"

DEFAULT_GOAL = "Apply for 1 day of casual leave on 2027-11-20 and notify my manager."   # any weekday after today works
SYSTEM = "You are an HR assistant. Use the tools to complete the goal."


def list_tools():
    async def go():
        async with Client(URL) as hr_mcp_client:
            return await hr_mcp_client.list_tools()
    return asyncio.run(go())


def call_tool(name, args):
    async def go():
        async with Client(URL) as hr_mcp_client:
            return await hr_mcp_client.call_tool(name, args, raise_on_error=False)
    return asyncio.run(go()).content[0].text


def main(goal):
    # 1. Ask the server what tools it has, and turn them into the format OpenAI expects.
    all_tools = list_tools()
    
    tools = [
        {"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.input_schema}}
        for t in all_tools
    ]
    print("tools from server:", [t["function"]["name"] for t in tools], "\n")

    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": goal}]

    # 2. The agent loop: model answers -> if it asked for tools, run them -> repeat.
    for _ in range(8):
        reply = llm.chat.completions.create(model=MODEL, messages=messages, tools=tools).choices[0].message
        messages.append(reply.model_dump(exclude_none=True))

        if not reply.tool_calls:                            # no tool wanted: the model is done
            print("\nANSWER:", reply.content)
            return

        for call in reply.tool_calls:
            args = json.loads(call.function.arguments)
            # 3. The model only asks. We run the tool on the server over MCP.
            text = call_tool(call.function.name, args)
            print(f"{call.function.name}({args}) -> {text}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": text})

    print("Stopped: too many steps.")


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or DEFAULT_GOAL)
