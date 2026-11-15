# its while loop with interactions with llm+ tool calls, it will keep on running untill there are no further tool calls
# it will use core functions like LLM api calls
#
# Local tools (time / weather) + every tool exposed by the Swiggy Food MCP server
# are offered to the LLM. Swiggy tool calls are forwarded to the MCP server.
#
# Usage:
#   python agent.py                      -> interactive chat (multi-turn, needed for ordering)
#   python agent.py "find biryani near me" -> single prompt
import asyncio
import json
import os
import sys
from datetime import datetime

import httpx
from dotenv import load_dotenv
from mcp import Client
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SWIGGY_MCP_URL = "https://mcp.swiggy.com/food"
SWIGGY_TOKEN = os.environ["SWIGGY_MCP_SERVER_TOKEN"]

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

# Tools that spend money / are irreversible -> ask the human before running them
CONFIRM_BEFORE_RUN = {"place_food_order"}
# Swiggy widget-internal tools that are not meant for conversational use
SKIP_MCP_TOOLS = {"get_food_delivery_status"}
MAX_TOOL_RESULT_CHARS = 20000

SYSTEM_PROMPT = """you are helpful assitant that can also order food on Swiggy for the user.
Swiggy ordering flow:
1. get_addresses -> ask the user which address to deliver to (unless only one / user already said).
2. search_restaurants / search_menu / get_restaurant_menu using that addressId.
3. update_food_cart with the chosen items, then get_food_cart to show items + total bill.
   If an item has variants (size/portion), pass the variant the user wants explicitly - otherwise Swiggy
   picks a default (e.g. a family pack). Always check the cart matches what was asked before moving on.
4. get_payment_options, ask the user which payment method they want.
5. Only call place_food_order after the user has explicitly confirmed the cart, address, total and payment method.
Never invent IDs - only use IDs returned by tools. Keep replies short and show prices in rupees."""

LOCAL_TOOLS = [
   {
      "type":"function",
      "function":{
         "name":"get_current_time",
         "description":"Get the current local date and time",
         "parameters":{"type":"object", "properties":{}},
      }
   },
   {
         "type":"function",
         "function":{
            "name":"get_lat_long_for_city",
            "description":"Get the latitude and longitude for a given city",
            "parameters":{
               "type":"object",
               "properties":{
                  "city":{
                     "type":"string",
                     "description":"Name of the city"
                  }
               },
               "required":[
                  "city"
               ]
            },
         }
      },
   {
            "type":"function",
            "function":{
               "name":"get_weather_for_lat_long",
               "description":"get weather for given latitude and longitude",
               "parameters":{
                  "type":"object",
                  "properties":{
                     "latitude":{
                        "type":"number",
                        "description":"Latitude of the location"
                     },
                     "longitude":{
                        "type":"number",
                        "description":"Longitude of the location"
                     }
                  },
                  "required":[
                     "latitude",
                     "longitude"
                  ]
               },
            }
         }
   ]
LOCAL_TOOL_NAMES = {t["function"]["name"] for t in LOCAL_TOOLS}


def mcp_tool_to_openai(tool):
    """Convert an MCP tool definition into OpenAI function-calling format."""
    schema = dict(tool.input_schema or {"type": "object", "properties": {}})
    # OpenAI rejects top-level anyOf/oneOf/... (Swiggy uses anyOf for "addressId OR lat+long")
    for key in ("anyOf", "oneOf", "allOf", "not", "enum", "const"):
        schema.pop(key, None)
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            # OpenAI caps function descriptions at 1024 chars
            "description": (tool.description or "")[:1024],
            "parameters": schema,
        },
    }


async def llm_call(http, messages, tools):
    data = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": tools
    }
    print(f"[llm] sending {len(messages)} messages, {len(tools)} tools")
    response = await http.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    return response.json()


def get_tools(result):
    if "choices" in result and len(result["choices"]) > 0:
        message = result["choices"][0]["message"]
        if message.get("tool_calls"):
            return message["tool_calls"]
    return []


async def execute_tools(mcp_client, tools):
    print("Number of tools recommended:", len(tools))
    results = []
    for tool in tools:
        id = tool.get("id")
        name = tool["function"]["name"]
        try:
            args = json.loads(tool["function"].get("arguments") or "{}")
        except json.JSONDecodeError:
            args = {}
        print(f"Executing tool: {name} with id: {id} args: {json.dumps(args)}")
        response = await execute_tool_by_name(mcp_client, name, args)
        print(f"  -> {response[:300]}{'...' if len(response) > 300 else ''}")
        results.append({"tool_call_id": id, "response": response})
    return results


async def execute_tool_by_name(mcp_client, name, args):
    if name in LOCAL_TOOL_NAMES:
        return execute_local_tool(name, args)

    if name in CONFIRM_BEFORE_RUN:
        print(f"\n⚠️  The agent wants to run {name} with:\n{json.dumps(args, indent=2)}")
        answer = (await asyncio.to_thread(input, "Really place this order? (y/N): ")).strip().lower()
        if answer != "y":
            return json.dumps({"error": "User declined. Order was NOT placed."})

    try:
        result = await mcp_client.call_tool(name, args)
    except Exception as e:
        return json.dumps({"error": f"MCP tool {name} failed: {e}"})

    text = "\n".join(c.text for c in result.content if getattr(c, "text", None))
    if not text and getattr(result, "structured_content", None):
        text = json.dumps(result.structured_content)
    if getattr(result, "is_error", False):
        text = f"ERROR: {text}"
    return text[:MAX_TOOL_RESULT_CHARS] or "(empty result)"


def execute_local_tool(name, args):
    if name == "get_current_time":
        return json.dumps({"current_time": datetime.now().isoformat()})
    elif name == "get_lat_long_for_city":
        # Mock implementation, replace with actual logic
        return json.dumps({"latitude": 12.9716, "longitude": 77.5946})
    elif name == "get_weather_for_lat_long":
        # Mock implementation, replace with actual logic
        return json.dumps({"temperature": 25, "condition": "Sunny"})
    return f"Tool {name} not recognized."


async def run_agent_loop(http, mcp_client, tools, messages):
    """Runs LLM <-> tool calls until the LLM stops asking for tools. Mutates `messages`."""
    result = await llm_call(http, messages, tools)
    tool_calls = get_tools(result)
    while len(tool_calls) > 0:
        messages.append(result["choices"][0]["message"])
        tool_call_result = await execute_tools(mcp_client, tool_calls)
        for r in tool_call_result:
            messages.append({"role": "tool", "content": r["response"], "tool_call_id": r["tool_call_id"]})
        result = await llm_call(http, messages, tools)
        tool_calls = get_tools(result)
    message = result["choices"][0]["message"]
    messages.append(message)
    return message.get("content")


async def main():
    async with httpx.AsyncClient(timeout=60) as http, \
            create_mcp_http_client(headers={"Authorization": f"Bearer {SWIGGY_TOKEN}"}) as mcp_http:
        async with Client(streamable_http_client(SWIGGY_MCP_URL, http_client=mcp_http)) as mcp_client:
            # pull all tools from swiggy server and add into existing tools
            mcp_tools = (await mcp_client.list_tools()).tools
            tools = LOCAL_TOOLS + [mcp_tool_to_openai(t) for t in mcp_tools if t.name not in SKIP_MCP_TOOLS]
            print(f"Loaded {len(tools)} tools ({len(tools) - len(LOCAL_TOOLS)} from Swiggy MCP)")

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            if len(sys.argv) > 1:
                messages.append({"role": "user", "content": " ".join(sys.argv[1:])})
                print("\nAssistant:", await run_agent_loop(http, mcp_client, tools, messages))
                return

            while True:
                try:
                    prompt = (await asyncio.to_thread(input, "\nYou: ")).strip()
                except (EOFError, KeyboardInterrupt):
                    break
                if prompt.lower() in {"exit", "quit"}:
                    break
                if not prompt:
                    continue
                messages.append({"role": "user", "content": prompt})
                print("\nAssistant:", await run_agent_loop(http, mcp_client, tools, messages))


if __name__ == "__main__":
    asyncio.run(main())
