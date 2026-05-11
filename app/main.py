from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.services.agent import conversational_agent


# =========================================================
# FASTAPI INIT
# =========================================================

app = FastAPI()


# =========================================================
# REQUEST SCHEMA
# =========================================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# =========================================================
# HEALTH ENDPOINT
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================================================
# CHAT ENDPOINT
# =========================================================

@app.post("/chat")
def chat(request: ChatRequest):

    # Get latest user message
    conversation_text = " ".join(
    [msg.content for msg in request.messages]
)

    response = conversational_agent(conversation_text)

    return response