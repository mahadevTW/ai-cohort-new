# its while loop with interactions with llm+ tool calls, it will keep on running untill there are no further tool calls
# it will use core functions like LLM api calls
import httpx
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = httpx.Client(timeout=60)
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


TOOLS = [
   {
      "type":"function",
      "function":{
         "name":"get_current_time",
         "description":"Get the current local date and time",
         "parameters":{
            
         },
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

def llm_call(messages = []):
    data = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": TOOLS
    }
    print("request body getting sent to llm ", data)
    response = client.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    r = response.json()
    return r

def run_agent_loop(prompt = ""):
    messages = [
        {"role": "system", "content": "you are helpful assitant "},
        {"role": "user", "content": prompt}
    ]
    result = llm_call(messages=messages)
    tools = get_tools(result)
    while(len(tools) > 0):
        print("Inside loop", tools)
        tool_call_result = execute_tools(tools)
        respnse_message = result["choices"][0]["message"]
        print("Response message:", respnse_message)
        messages.append(respnse_message)
        print("Tool call results:", tool_call_result)
        for r in tool_call_result:
            messages.append({"role": "tool", "content": r["response"], "tool_call_id": r.get("tool_call_id")})
        result = llm_call(messages=messages)
        tools = get_tools(result)
    # process the result, read the response from result and print it
    message = result["choices"][0]["message"]
    print("final message:", message)

def get_tools(result):
    if "choices" in result and len(result["choices"]) > 0:
        message = result["choices"][0]["message"]
        if "tool_calls" in message:
            return message["tool_calls"]
    return []

def execute_tools(tools):
    print("Number of tools recommended:", len(tools))
    results = []
    for tool in tools:
        id = tool.get("id")
        name = tool.get("function").get("name")
        print(f"Executing tool: {name} with id: {id}")
        respponse = execute_tool_by_name(name)  # Assuming you have a function to execute the tool by its name
        results.append({"tool_call_id": id, "response": respponse})
    return results


def execute_tool_by_name(name):
    if name == "get_current_time":
        import json
        from datetime import datetime
        return json.dumps({"current_time": datetime.now().isoformat()})
    elif name == "get_lat_long_for_city":
        # Mock implementation, replace with actual logic
        return json.dumps({"latitude": 12.9716, "longitude": 77.5946})
    elif name == "get_weather_for_lat_long":
        # Mock implementation, replace with actual logic
        return json.dumps({"temperature": 25, "condition": "Sunny"})
    else:
        return f"Tool {name} not recognized."

run_agent_loop("how is the weather in Bangalore")