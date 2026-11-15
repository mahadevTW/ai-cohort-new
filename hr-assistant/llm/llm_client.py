import json

import httpx
import os
from db.db import list_messages_in_conversation,read_messages_after_last_compaction,get_conversation_summary,update_conversation_summary
from llm.tools import execute_tools
MESSAGE_LIMIT = 5
token_usage = [{"in":1, "out":1}]
from embed import find_relevant_chunks
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
            "name":"get_current_logged_in_employee_details",
            "description":"Get the details of the currently logged in employee",
            "parameters":{
            },
         }
      }, 
   {
            "type":"function",
            "function":{
               "name":"get_leave_balance",
               "description":"Get the leave balance of the for given employee id",
               "parameters":{
                   "type":"object",
                   "properties":{
                       "employee_id": {
                           "type": "string"
                       }
                   }
               },
            }
         },
   {
               "type":"function",
               "function":{
                  "name":"apply_leave",
                  "description":"Apply leave for the currently logged in employee",
                  "parameters":{
                      "type":"object",
                      "properties":{
                          "employee_id": {
                              "type": "string"
                          },
                          "start_date": {
                              "type": "string"
                          },
                          "end_date": {
                              "type": "string"
                          },
                          "leave_type": {
                              "type": "string"
                          }
                      }
                  },
               }
            }, 
   {
                  "type":"function",
                  "function":{
                     "name":"send_email",
                     "description":"Send an email to the person for given email subject and body",
                     "parameters":{
                         "type":"object",
                         "properties":{
                             "email_id": {
                                 "type": "string"
                             },
                             "subject": {
                                 "type": "string"
                             },
                             "body": {
                                 "type": "string"
                             }
                         }
                     },
                  }
               },    
]



    
    # print(f"Relevant chunks for query: {query}, found {len(relevant_chunks)} chunks.")
    # for chunk in relevant_chunks:
    #     print(chunk)
def enrich_prompt(prompt: str) -> str:
    # this will read relevent chunk from choma db and attach it to the original prompt
    relevant_chunks = find_relevant_chunks(prompt)
    top_chunk = relevant_chunks[0] if relevant_chunks else ""
    enriched_prompt = f"here is the relevent infomation from my internal policy DB for below question:{top_chunk['text']}, Question : {prompt}"
    return enriched_prompt


def make_llm_api_call(messages,tools):
    data = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": tools
    }
    # print("request body sent to LLM:", data)
    response = client.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    r = response.json()
    return r

def call_llm(prompt, conversation_id: str=None):
    # Prompt Caching:
    # see if there is same question stored in chroma db stored as conversations
    # if they are found then we can read the prev answer the question and send it back without calling the LLM
    # response  = find_responses_in_cache(prompt)  # hypothetical function to check if the response is already cached
    # if response:
    #     return response
    
    # enrich chunk with relevent information:
    # dont read all messages, but only read messages after last compaction was done
    # last compaction is identified by the last_message_id in the conversation summary table
    enriched_prompt = enrich_prompt(prompt)
    # ensure_conversation_exists
    if conversation_id is None:
        from db.db import create_conversation
        conversation = create_conversation(title=prompt)
        conversation_id = conversation.id

    conversation_history = read_messages_after_last_compaction(conversation_id=conversation_id)
    conversation_summary = get_conversation_summary(conversation_id=conversation_id)
    
    summary_message = None
    if conversation_summary:
        summary_message = conversation_summary.summary_text

    if len(conversation_history) > MESSAGE_LIMIT:
        print(f"triggering the compaction after exceeding the message limit, current length is  : {len(conversation_history)}")
        compaction_result = compact_conversation(conversation_id)
        update_conversation_summary(conversation_id=conversation_id, summary_text=compaction_result["summary"], last_message_id=compaction_result["last_message_id"])
    r = make_llm_api_call(
        messages=[
            {"role": "system", "content": "You are a helpful assistant for my company Rebind Rise, you can only answer questions related to HR and only based on context passed for the question in prompt, avoid answering anything outside of the provided context."},
            {"role":"developer", "content": f"here is summary of conversation so far {summary_message}"},
            *[{"role": m["role"], "content": m["content"]} for m in conversation_history],
            {"role": "user", "content": enriched_prompt}
        ],
        tools=TOOLS
    )
    
    # check if there is a tool call in the response
    llm_response = r["choices"][0]["message"]
    print(f"LLM raw response: {llm_response}")
    while "tool_calls" in llm_response:
        tool_calls  = llm_response["tool_calls"]
        tool_call_response = []
        for tool_call in tool_calls:
            print(f"Tool suggested: {tool_call}")
            print(f"************* tool call sugested + {tool_call}")
            tool_call_id =  tool_call["id"]
            result = execute_tools(tool_call)
            print(f"Tool call result: {result}")
            print(f"Tool call ID: {tool_call_id}")
            tool_call_response.append({"role":"tool", "content": json.dumps(result),"tool_call_id": tool_call_id})
        
        r = make_llm_api_call(
            messages=[
                {"role": "system", "content": "You are a helpful assistant for my company Rebind Rise, you can only answer questions related to HR and only based on context passed for the question in prompt, avoid answering anything outside of the provided context."},
                {"role":"developer", "content": f"here is summary of conversation so far {summary_message}"},
                *[{"role": m["role"], "content": m["content"]} for m in conversation_history],
                {"role": "user", "content": enriched_prompt},
                llm_response,
                *tool_call_response,
            ],
            tools=TOOLS
        )
        llm_response = r["choices"][0]["message"]
    return {"content": llm_response["content"], "input_tokens": 0, "output_tokens": 0, "conversation_id": conversation_id}
    
        
        
    # print(f"LLM response: {llm_response}")
    
    # cache the response for future use
    # cache_response(prompt, llm_response["content"])  # hypothetical function to cache the response
    
    # log number of input and output tokens being used
    input_tokens = r["usage"]["prompt_tokens"]
    output_tokens = r["usage"]["completion_tokens"]
    print(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
    return {"content": llm_response["content"], "input_tokens": input_tokens, "output_tokens": output_tokens, "conversation_id": conversation_id}

def compact_conversation(conversation_id):
    conversation_history = list_messages_in_conversation(conversation_id=conversation_id)
    # compaction prompt to summarize the conversation
    PROMPT = f"Summarize the following conversation:\n{json.dumps(conversation_history)}, make sure you dont miss the facts like location, name, dates and any facutal data present inside the conversation. summary should not be more that 100 words"
    api_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": PROMPT}
        ],
    }
    response = client.post(url, headers=headers, json=api_body)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    r = response.json()
    summary = r["choices"][0]["message"]["content"]
    last_message = conversation_history[-1] if conversation_history else None
    print(f"Last message in conversation: {last_message}")
    last_message_id = conversation_history[-1]["id"] if conversation_history else None
    
    # log the compaction token usage
    input_tokens = r["usage"]["prompt_tokens"]
    output_tokens = r["usage"]["completion_tokens"]
    print(f"Compaction - Input tokens: {input_tokens}, Output tokens: {output_tokens}")
    
    return {"summary": summary, "last_message_id": last_message_id}
    