from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

from .memory import (
    initialize_memory,
    save_message,
    get_history
)
from .personality import load_personality
from .ai_engine import generate_response

app = FastAPI(
    title="MACID_AI",
    description="Private Local AI Assistant",
    version="0.1.0"
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.on_event("startup")
def startup():
    initialize_memory()


@app.get("/")
def home():
    return {
        "name": "MACID_AI",
        "status": "online",
        "mode": "local"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "engine": "MACID_AI"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())

    try:
        history = get_history(session_id)

        messages = [
            {
                "role": "system",
                "content": load_personality()
            }
        ]

        messages.extend(history)
        messages.append({
            "role": "user",
            "content": request.message
        })

        save_message(
            session_id,
            "user",
            request.message
        )

        answer = generate_response(messages)

        save_message(
            session_id,
            "assistant",
            answer
        )

        return {
            "session_id": session_id,
            "response": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )
