from db.db import insert_message, get_all_messages
from service.vector_utils import build_context
import httpx
class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.http_client = httpx.Client(timeout=10)

    def chat(self, message, conversation_id=None):
        # 1. for this question , query the chroma db for top 3 relevent chunks
        # 2. Build context based on the retrieved chunks and pass the updated context + question to the LLM
        # 3. Create variable message_with_context 
        # 4. update APi call to pass message_with_context rather than message
        context = build_context(message)
        message_with_context = f"Context:\n{context}\n\nQuestion: {message}"
        conversation_history = get_all_messages(conversation_id)
        c = []
        for m in conversation_history:
            c.append({"role": m.role, "content": m.content})
        print(f"context generated before passing to llm : {message_with_context}")
        response = self.http_client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are HR assitent to Rebind Rise, answer policy related quetions based on provided context only, if the context is not enough to answer, say You dont know politly, do not generate answers for policy based on your knolewdge"},
                    * c,
                    {"role": "user", "content": message_with_context}
                    ]
            }
        )
        r = response.json()
        usage = r.get("usage", {})
        
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        print("input tokens:"+ str(usage.get("prompt_tokens", 0)))
        print("output tokens:"+ str(usage.get("completion_tokens", 0)))
        print("total tokens:"+ str(usage.get("total_tokens", 0)))
        
        response = r["choices"][0]["message"]["content"]
        # self.conversation_history.append({"role": "user", "content": message})
        # self.conversation_history.append({"role":"assistant", "content": response})
        insert_message("user", message, input_tokens,conversation_id=conversation_id)
        insert_message("assistant", response, output_tokens,conversation_id=conversation_id)
        return response
        