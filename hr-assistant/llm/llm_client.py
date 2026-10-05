import json

import httpx
import os
from db.db import list_messages_in_conversation,read_messages_after_last_compaction,get_conversation_summary,update_conversation_summary
MESSAGE_LIMIT = 5
token_usage = [{"in":1, "out":1}]
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = httpx.Client(timeout=60)
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
def call_llm(prompt, conversation_id: str=None):
    # dont read all messages, but only read messages after last compaction was done
    # last compaction is identified by the last_message_id in the conversation summary table
    
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

    # if number of messages in the conversation history exceeds a certain limit, trigger compaction
    if len(conversation_history) > MESSAGE_LIMIT:
        print(f"triggering the compaction after exceeding the message limit, current length is  : {len(conversation_history)}")
        compaction_result = compact_conversation(conversation_id)
        # save the compaction result to the conversation_summary table
        # compaction_result["summary"], compaction_result["last_message_id"]
        update_conversation_summary(conversation_id=conversation_id, summary_text=compaction_result["summary"], last_message_id=compaction_result["last_message_id"])
        
    # when compaction occurs, pass truncated conversation history to the LLM
    # when compaction does not occur , check if there is existing summary saved into db
    # read summary and the all messages after the last_message_id in conversation sumamry
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role":"developer", "content": f"here is summary of conversation so far {summary_message}"}, # pass summary text as one of the message into the api call
            *[{"role": m["role"], "content": m["content"]} for m in conversation_history],
            {"role": "user", "content": prompt}
            ],
    }
    print("request body sent to LLM:", data)
    response = client.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    r = response.json()
    llm_response = r["choices"][0]["message"]
    print(f"LLM response: {llm_response}")
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
    