from fastapi import FastAPI
import httpx
app  = FastAPI()
OPENAI_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
import os
OPENAI_API_KEY =  os.getenv("OPENAI_API_KEY")
@app.get("/")
async def hello():
    return {"message": "Hello, HR Assistant!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/chat")
async def chat(message:str):
    # use httpx module to file chat endpoint of the OpenAI API and whatever response comes from Open ai send it back to user
    response = httpx.post(
        OPENAI_CHAT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message}]
        }
    )
    chat_response = response.json()
    #  extract the actual response
    chat_response = chat_response["choices"][0]["message"]["content"]
    return {"response": chat_response} 


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)