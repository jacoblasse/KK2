from pydantic import BaseModel

class PromptBuilderInput(BaseModel):
    question: str
    stats_summary: str

class PromptBuilderOutput(BaseModel):
    prompt: str


class ResponseParserOutput(BaseModel):
    prompt: str
    answer: str
    model: str = "HuggingFaceTB/SmolLM2-135M-Instruct"