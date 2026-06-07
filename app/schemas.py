from pydantic import BaseModel
from app.config import settings

class UploadResponse(BaseModel):
    rows: int
    columns: list[str]
    dtypes: dict[str, str]



class StatsResponse(BaseModel):
    stats: dict[str, dict[str, float]]


class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    question: str
    answer: str
    model: str = settings.llm_name

