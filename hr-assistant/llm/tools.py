import json
MCP_URL = "http://127.0.0.1:8765/mcp"
from fastmcp import Client
import asyncio

# run given tool of mcp server respresented by MCP_URL
def call_MCP_tool(name, args):
    async def go():
        async with Client(MCP_URL) as hr_mcp_client:
            return await hr_mcp_client.call_tool(name, args, raise_on_error=False)
    return asyncio.run(go()).content[0].text

def execute_tools(tool):
    # is tool coming as response is part of MCP server
    # then call execute_tool and get the response back
    # 
    tool_name = tool["function"]["name"]
    if tool_name == "get_current_time":
        from datetime import datetime
        return {"current_time": datetime.now().isoformat()}
    if tool_name == "get_current_logged_in_employee_details":
        from llm.leave_mgmt import get_logged_in_employee_details
        details = get_logged_in_employee_details()
        return {"employee_details": details}
    else:
        # apart from this tools all tools are hosted on mcp server
        # call execute tool function on mcp server
        args = tool["function"]["arguments"]
        if isinstance(args, str):
            args = json.loads(args)
        return call_MCP_tool(tool_name, args)