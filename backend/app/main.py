import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import AsyncClient

from backend.app.memory import (
    initialize_memory,
    save_message,
    get_history
)

load_dotenv()

app = FastAPI(
    title="MACID_AI",
    description="Private local AI assistant",
    version="0.1.0"
)

ollama = AsyncClient(
    host=os.getenv("OLLAMA_URL", "http://localhost:11434")
)

MODEL = os.getenv("MODEL_NAME", "qwen2.5:1.5b")

SYSTEM_PROMPT_PATH = Path(
    os.getenv("SYSTEM_PROMPT_PATH", "/app/config/personality.txt")
)


def load_personality():
    try:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "You are MACID_AI, a helpful private AI assistant."


@app.on_event("startup")
async def startup():
    initialize_memory()


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/health")
async def health():
    return {
        "status": "online",
        "name": "MACID_AI"
    }


@app.get("/history/{session_id}")
async def conversation_history(session_id: str):
    try:
        history = get_history(session_id, limit=100)

        return {
            "session_id": session_id,
            "messages": history
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not load conversation history: {error}"
        )


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        history = get_history(request.session_id, limit=20)

        messages = [
            {
                "role": "system",
                "content": load_personality()
            },
            *history,
            {
                "role": "user",
                "content": request.message
            }
        ]

        response = await ollama.chat(
            model=MODEL,
            messages=messages
        )

        answer = response["message"]["content"]

        save_message(
            request.session_id,
            "user",
            request.message
        )

        save_message(
            request.session_id,
            "assistant",
            answer
        )

        return {
            "response": answer,
            "session_id": request.session_id
        }

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"AI engine unavailable: {error}"
        )
