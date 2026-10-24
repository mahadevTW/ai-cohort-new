import httpx
class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.http_client = httpx.Client(timeout=10)

    def chat(self, message):
        response = self.http_client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": message}]
            }
        )
        r = response.json()
        return r["choices"][0]["message"]["content"]
        