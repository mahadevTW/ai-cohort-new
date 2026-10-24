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
app  = FastAPI()
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAIClient(api_key=api_key)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"title": "Chat Assistant", "name":"mahadev"})


@app.get("/chat")
def chat(message:str="hello"):
    chat_response = openai_client.chat(message)
    return {"message": chat_response}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000,reload=True)