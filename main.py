from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os 

app = FastAPI()

api_key = os.getenv("GROQ_API_KEY")
class Message(BaseModel):
    name: str
    content: str

@app.post("/chat")
def chat(msg: Message):

    messages = [
        {
            "role": "system",
            "content": f"""
            You are a medical care assistant.
            You answer in Arabic about medical care.
            You will try to understand the user's name: {msg.name}.
            If you don't know the answer, say you don't know.
            """
        },
        {
            "role": "user",
            "content": msg.content
        }
    ]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": messages
        }
    )

    result = response.json()

    if "choices" in result:
        reply = result["choices"][0]["message"]["content"]
        return {"reply": reply}
    else:
        return {"error": result}