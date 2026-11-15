# Write the apis using some fremework so that you can expose
# Run this api under some web server
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from service.llm_service import OpenAIClient
from dotenv import load_dotenv
from pathlib import Path
import uvicorn
import os
from db.models import Message
from db.db import get_all_messages,create_conversation,list_conversations
app  = FastAPI()
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAIClient(api_key=api_key)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"title": "Rebind Rise", "name":"mahadev"})


@app.get("/chat")
def chat(message:str="hello", conversation_id:str = None):
    # detect keywords from message --> ????
    # pass keywords to file and extract all matching lines
    # pass this matched lines to llm
    # let llm answer
    if not conversation_id:
        conversation_id = None
        conversation = create_conversation(message)
        print("Created new conversation with ID:", conversation.id)
        conversation_id = conversation.id
    chat_response = openai_client.chat(message,conversation_id)
    return {"message": chat_response,"conversation_id": conversation_id}

@app.get("/messages")
def get_messages(conversation_id: str):
    messages = get_all_messages(conversation_id)
    return {"messages": [{"role": m.role, "content": m.content, "conversation_id": m.conversation_id} for m in messages]}

@app.get("/conversations")
def get_conversations():
    conversations = list_conversations()
    return {"conversations": [{"id": c.id, "title": c.title,"time": c.timestamp} for c in conversations]}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000,reload=True)