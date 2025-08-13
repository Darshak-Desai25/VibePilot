from typing import TypedDict

from langchain.schema import Document
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    question: str
    messages: list[BaseMessage]
    prompt: str
    context: list[Document]
    answer: str
    social_media: str
    clear_query: str
    on_topic: str
    image_link: str

from pydantic import BaseModel

class Answer(BaseModel):
    image: str
    caption: str

class ChatResponse(BaseModel):
    answer: Answer  # ✅ Now `answer` must be a dictionary with `image` and `caption`
