import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import AsyncClient

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


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
async def health():
    return {
        "status": "online",
        "name": "MACID_AI"
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": load_personality()
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        )

        return {
            "response": response["message"]["content"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"AI engine unavailable: {error}"
        )