from pydantic import BaseModel
from app.config import settings
from app.chain.runnable import Runnable, RunnableLambda, RunnableSequence

class LLMRunnerOutput(BaseModel):
    raw_test: str

class PromptBuilderInput(BaseModel):
    question: str
    stats_summary: str

class PromptBuilderOutput(BaseModel):
    prompt: str


class ResponseParserOutput(BaseModel):
    prompt: str
    answer: str
    model: str = settings.llm_name


class PromptBuilder(Runnable[PromptBuilderInput, PromptBuilderOutput]):
    def invoke(self, data: PromptBuilderInput) -> PromptBuilderOutput:
        prompt = f"Du är en dataanalytiker som hjälper till att svara på frågor baserat på datasetets statistik. Fråga: {data.question} Stats: {data.stats_summary} Svara på frågan baserat på statistiken. "
    
        return PromptBuilderOutput(prompt=prompt)