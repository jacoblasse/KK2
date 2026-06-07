from pydantic import BaseModel
from app.config import settings

class PromptBuilderInput(BaseModel):
    question: str
    stats_summary: str

class PromptBuilderOutput(BaseModel):
    prompt: str


class ResponseParserOutput(BaseModel):
    prompt: str
    answer: str
    model: str = settings.llm_name