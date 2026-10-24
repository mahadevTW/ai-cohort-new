from db.db import insert_message, get_all_messages

import httpx
class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.http_client = httpx.Client(timeout=10)

    def chat(self, message):
        conversation_history = get_all_messages()
        c = []
        for m in conversation_history:
            c.append({"role": m.role, "content": m.content})

        response = self.http_client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    * c,
                    {"role": "user", "content": message}
                    ]
            }
        )
        r = response.json()
        response = r["choices"][0]["message"]["content"]
        # self.conversation_history.append({"role": "user", "content": message})
        # self.conversation_history.append({"role":"assistant", "content": response})
        insert_message("user", message)
        insert_message("assistant", response)
        return response
        