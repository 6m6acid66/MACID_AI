import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen2.5:1.5b"
)

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(BASE_DIR / "data" / "macid_ai.sqlite3")
)

SYSTEM_PROMPT_PATH = os.getenv(
    "SYSTEM_PROMPT_PATH",
    str(BASE_DIR / "config" / "personality.txt")
)