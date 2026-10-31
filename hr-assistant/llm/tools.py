import json


def execute_tools(tool):
    tool_name = tool["function"]["name"]
    if tool_name == "get_current_time":
        from datetime import datetime
        return {"current_time": datetime.now().isoformat()}
    if tool_name == "send_email":
        from llm.leave_mgmt import send_email
        args = tool["function"]["arguments"]
        json_str = json.loads(args)
        email_id = json_str["email_id"]
        subject = json_str["subject"]
        body = json_str["body"]
        send_email(email_id, subject, body)
        return {"status": "email_sent"}
    if tool_name == "apply_leave":
        from llm.leave_mgmt import apply_leave
        args = tool["function"]["arguments"]
        json_str = json.loads(args)
        employee_id = json_str["employee_id"]
        start_date = json_str["start_date"]
        end_date = json_str["end_date"]
        leave_type = json_str["leave_type"]
        apply_leave(employee_id, start_date, end_date, leave_type)
        return {"status": "leave_applied"}
    if tool_name == "get_current_logged_in_employee_details":
        from llm.leave_mgmt import get_logged_in_employee_details
        details = get_logged_in_employee_details()
        return {"employee_details": details}
    if tool_name == "get_leave_balance":
        from llm.leave_mgmt import get_leave_balance
        print(f"Leave Balance tool input : {tool}")
        args = tool["function"]["arguments"]
        json_str = json.loads(args)
        balance = get_leave_balance(json_str["employee_id"])
        return {"leave_balance": balance}
    if tool_name == "send_email":
        from llm.leave_mgmt import send_email
        args = tool["function"]["arguments"]
        json_str = json.loads(args)
        email_id = json_str["email_id"]
        subject = json_str["subject"]
        body = json_str["body"]
        send_email(email_id, subject, body)
        return {"status": "email_sent"}
    raise ValueError(f"Unknown tool: {tool_name}")