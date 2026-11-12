
from fastapi import FastAPI

app = FastAPI(
    title="MACID_AI",
    description="Private Local AI Assistant",
    version="0.1.0"
)


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
