# Create virtual environment using the following command:
# run the server using python hr-assitant-2/main.py
# make sure to set the OPENAI_API_KEY environment variable before running the server
# use export OPENAI_API_KEY="your_api_key_here"

from fastapi import FastAPI
import httpx
app  = FastAPI()
import os
from db.models import autocreate_tables

OPENAI_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY =  os.getenv("OPENAI_API_KEY")
@app.get("/")
async def hello():
    return {"message": "Hello, HR Assistant!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# conversation_history = []
@app.get("/chat")
async def chat(message:str):
    # use httpx  module to file chat endpoint of the OpenAI API and whatever response comes from Open ai send it back to user
    # easy way
    # conversation_history.append({"role": "user", "content": message})
    # above line will be replaced with actual db insert query
    from db.db import insert_message
    insert_message(role="user", content=message)
    
    # read conversation history from db
    from db.db import list_messages
    messages = list_messages()
    # create conversation history from messages
    ch = []
    for msg in messages:
        ch.append({"role": msg.role, "content": msg.content})
    
    print(f"Conversation history getting sent to llm: {ch}")
    response = httpx.post(
        OPENAI_CHAT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            # "messages": conversation_history
            # this should be replaced with history coming from db
            "messages": ch
        }
    )
    chat_response = response.json()
    #  extract the actual response
    chat_response = chat_response["choices"][0]["message"]["content"]
    # add assistant response to conversation_history
    # conversation_history.append({"role": "assistant", "content": chat_response})
    insert_message(role="assistant", content=chat_response)
    
    return {"response": chat_response} 


if __name__=="__main__":
    autocreate_tables()
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)