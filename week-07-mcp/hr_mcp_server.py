"""A tiny HR server. It offers four tools to any MCP client, over HTTP.

Start it once, in its own terminal, and leave it running:
    ./.venv/bin/python week-07-mcp/hr_mcp_server.py
Clients connect to  http://127.0.0.1:8765/mcp . It sits quietly and waits for requests. That is normal.
(Add --stdio to run the old way, where a client starts the server itself.)

Two rules:
  * Never print() here. Over stdio a print breaks the conversation; over HTTP it only clutters the log. Use stderr.
  * No tool takes an employee id. The server knows who is calling (Asha); the model is never asked.
"""

import sys
from datetime import date

from fastmcp import FastMCP

mcp = FastMCP("hr-desk")

ASHA = {"manager": "Ravi Menon", "casual_days": 4}
LEAVE_REQUESTS = []          # our fake HR system: a plain list
NOTIFICATIONS = []

READ_ONLY = {"readOnlyHint": True}       # a label the client can read: "this tool changes nothing"


@mcp.tool(annotations=READ_ONLY)
def get_leave_balance() -> dict:
    """Get how many casual leave days are left. Use it before applying for leave."""
    used = sum(r["days"] for r in LEAVE_REQUESTS)
    return {"casual_days_left": ASHA["casual_days"] - used}


@mcp.tool(annotations=READ_ONLY)
def get_holidays() -> list[str]:
    """List the upcoming company holidays."""
    return ["2026-12-25 Christmas", "2027-01-26 Republic Day"]


@mcp.tool
def apply_leave(start_date: str, days: int) -> dict | str:
    """Apply for casual leave. This WRITES to the HR system.
    start_date is YYYY-MM-DD and must be a weekday after today. Asking twice for the same dates is safe."""
    start = date.fromisoformat(start_date)
    if start <= date.today():
        return f"Error: start_date must be after today ({date.today()})"
    if start.weekday() >= 5:
        return f"Error: {start_date} is a {start.strftime('%A')}. Pick a weekday"
    request = {"id": len(LEAVE_REQUESTS) + 1, "start_date": start_date, "days": days}
    LEAVE_REQUESTS.append(request)
    print("saved leave request", request, file=sys.stderr)      # logs go to stderr, never stdout
    return {"request_id": request["id"], "status": "submitted"}


@mcp.tool
def notify_manager(request_id: int, note: str) -> dict | str:
    """Send the manager a short message about a leave request. This SENDS a message.
    Use it only after apply_leave worked, with the request_id it returned. Asking twice is safe."""
    if not any(r["id"] == request_id for r in LEAVE_REQUESTS):
        return f"Error: no leave request {request_id}. Call apply_leave first"
    if any(n["request_id"] == request_id for n in NOTIFICATIONS):
        return {"sent_to": ASHA["manager"], "status": "already_sent"}
    NOTIFICATIONS.append({"request_id": request_id, "note": note})
    return {"sent_to": ASHA["manager"], "status": "sent"}

if __name__ == "__main__":
    if "--stdio" in sys.argv:                                 # old style: the client starts the server itself (rarely used)
        mcp.run()
    else:                                                     # default: run it once, clients connect by URL
        mcp.run(transport="http", host="127.0.0.1", port=8765)    # URL: http://127.0.0.1:8765/mcp