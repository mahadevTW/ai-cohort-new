# Write the apis using some fremework so that you can expose
# Run this api under some web server
from fastapi import FastAPI
from service.llm_service import OpenAIClient
import uvicorn
import os
app  = FastAPI()
api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAIClient(api_key=api_key)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/chat")
def chat(message:str="hello"):
    chat_response = openai_client.chat(message)
    return {"message": chat_response}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000,reload=True)