from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    role: str


class QuestionResponse(BaseModel):
    answer: str