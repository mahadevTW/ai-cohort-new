# Create virtual environment using the following command:
# run the server using python hr-assitant-2/main.py
# make sure to set the OPENAI_API_KEY environment variable before running the server
# use export OPENAI_API_KEY="your_api_key_here"

import token

from fastapi import FastAPI
from db.db import create_conversation, increment_conversation_tokens, list_messages, get_summary, list_messages_after_summary
from db.db import insert_message
import httpx
app  = FastAPI()
import os
from db.models import autocreate_tables

OPENAI_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY =  os.getenv("OPENAI_API_KEY")
client  = httpx.Client(timeout=60)
@app.get("/")
async def hello():
    return {"message": "Hello, HR Assistant!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# conversation_history = []
@app.get("/chat")
async def chat(message:str, conversation_id: int =None):
    # use httpx  module to file chat endpoint of the OpenAI API and whatever response comes from Open ai send it back to user
    # easy way
    # conversation_history.append({"role": "user", "content": message})
    # above line will be replaced with actual db insert query
    if not conversation_id:
        c = create_conversation(message)
        conversation_id = c["id"]
    
    # read conversation history from db
    from db.db import list_messages
    summary_text = ""
    messages = []
    # case 1. there might be summary present into the summary table
        # read summary + messages after summary was done and use that to send to llm
    # case 2. there might not be summary present in summary table
        #  send all messages
    
    summary = get_summary(conversation_id=conversation_id)
    
    if summary:
        summary_text = summary.summary
        # set messages to be all messages after the summary was done
        messages  = list_messages_after_summary(conversation_id=conversation_id, last_message_id=summary.last_message_id)
    else:
        summary_text = ""
        messages = list_messages(conversation_id=conversation_id)
    
    if len(messages) >= 10:
        print(f"Compacting conversation as it has reached 10 or more messages. current len: {len(messages)}")
        compact_conversation(conversation_id=conversation_id)
    
    # create conversation history from messages
    ch = []
    if summary_text:
            ch.append({"role": "developer", "content": "here is summary of conversation till now: "+summary_text})
            
    for msg in messages:
        ch.append({"role": msg.role, "content": msg.content})
    
    ch.append({"role": "user", "content": message})
    print(f"Conversation history getting sent to llm: {ch}")
    
    
    response = client.post(
        OPENAI_CHAT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            # "messages": conversation_history
            # this should be replaced with history coming from db
            "messages": ch
        }
    )
    response = response.json()
    #  extract the actual response
    chat_response = response["choices"][0]["message"]["content"]
    
    # read input tokens and output tokens from the response
    input_tokens = response["usage"]["prompt_tokens"]
    output_tokens = response["usage"]["completion_tokens"]
    
    # add assistant response to conversation_history
    # conversation_history.append({"role": "assistant", "content": chat_response})
    insert_message(role="user", content=message, conversation_id=conversation_id,tokens=input_tokens)
    insert_message(role="assistant", content=chat_response, conversation_id=conversation_id, tokens=output_tokens)
    total_tokens = input_tokens + output_tokens
    print(f"Total tokens used in this  response generation: {total_tokens}, input tokens: {input_tokens}, output tokens: {output_tokens}")
    increment_conversation_tokens(conversation_id=conversation_id, tokens=total_tokens)
    
    
    return {"response": chat_response} 


def compact_conversation(conversation_id: int):
    # 1. list all messages for the conversation
    # 2. make llm call to summarize the conversation using the messages retrieved from the database
    # 3. store summary back into database along with last message id pulled in step 1
    messages = list_messages(conversation_id=conversation_id)
    ch = []
    for msg in messages:
        ch.append({"role": msg.role, "content": msg.content})
    
    response = client.post(
        OPENAI_CHAT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            # "messages": conversation_history
            # this should be replaced with history coming from db
            "messages": [{"role": "user", "content": "summarize the conversation for given messages, make sure you keep facts and importent information intact, remove pleasantries or unnecessary details. Here are the messages: " + str(ch)}]
        }
    )
    
    summary = response.json()["choices"][0]["message"]["content"]
    
    from db.db import insert_or_update_conversation_summary
    # insert the conversation summary into the database
    last_message_id = messages[len(messages)-1].id if messages else None
    insert_or_update_conversation_summary(conversation_id=conversation_id, summary=summary, last_message_id=last_message_id)
    return {"summary": summary}





if __name__=="__main__":
    autocreate_tables()
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)