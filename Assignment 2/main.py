from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from groq import Groq

app = FastAPI()

chat_sessions: Dict[str, List[dict]] = {}

client = Groq(api_key="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")

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: ChatRequest):

    if not data.session_id:
        session_id = f"session_{len(chat_sessions) + 1}"
        chat_sessions[session_id] = []
    else:
        session_id = data.session_id
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []

    messages = chat_sessions[session_id]

    messages.append({
        "role": "user",
        "content": data.message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    messages.append({
        "role": "assistant",
        "content": reply
    })

    return {
        "session_id": session_id,
        "response": reply
    }
