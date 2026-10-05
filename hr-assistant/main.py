from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from llm.llm_client import call_llm
from db.db import list_messages_in_conversation, create_conversation, create_chat_message, update_token_usage
import uvicorn

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"assistant_name": "HR Assistant"})

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/greet")
def greet(name: str="World"):
    return {"message": f"Hello, {name}!"}

@app.get("/chat")
def chat_with_hr_assistant(user_input: str, conversation_id: str=None):
    response = call_llm(user_input,conversation_id=conversation_id)
    # save user message and assistant response in the database
    # read in and out tokens
    create_chat_message(conversation_id=response["conversation_id"], text=user_input, role="user", tokens_spent=response["input_tokens"])
    create_chat_message(conversation_id=response["conversation_id"], text=response["content"], role="assistant", tokens_spent=response["output_tokens"])
    
    # update conversation with total tokens
    total_tokens = response["input_tokens"] + response["output_tokens"]
    update_token_usage(conversation_id=response["conversation_id"], tokens=total_tokens)
    
    # return the conversation id along with the response
    return {"response": response, "conversation_id": response["conversation_id"], "input_tokens": response["input_tokens"], "output_tokens": response["output_tokens"], "total_tokens": total_tokens}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)