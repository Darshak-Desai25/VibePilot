import uvicorn
from fastapi import FastAPI

from src.app.api.v1.endpoints.chat import router as chat_router

app = FastAPI(
    title="Chat API",
    description="An API for chat-based question answering using RAG workflow",
    version="1.0.0",
)

app.include_router(chat_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
import uvicorn
from fastapi import FastAPI

from src.app.api.v1.endpoints.chat import router as chat_router

app = FastAPI(
    title="Chat API",
    description="An API for chat-based question answering using RAG workflow",
    version="1.0.0",
)

app.include_router(chat_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

