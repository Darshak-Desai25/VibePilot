from pydantic import BaseModel



class Answer(BaseModel):
    image: str
    caption: str

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: Answer
