def execute_tools(tool):
    tool_name = tool["function"]["name"]
    if tool_name == "get_current_time":
        from datetime import datetime
        return {"current_time": datetime.now().isoformat()}
    else:
        raise ValueError(f"Unknown tool: {tool_name}")