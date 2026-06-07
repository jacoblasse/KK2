from pydantic import BaseModel
from app.config import settings
from app.chain.runnable import Runnable, RunnableLambda, RunnableSequence
from transformers import pipeline

class LLMRunnerOutput(BaseModel):
    raw_text: str

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
    
    
pipe = pipeline("text-generation", model=settings.llm_name)

class LLMRunner(Runnable[PromptBuilderOutput, LLMRunnerOutput]):
    def invoke(self, data: PromptBuilderOutput) -> LLMRunnerOutput:
        messages = [
            {"role":"user", "content":data.prompt}
        ]
        output = pipe(messages, max_new_tokens=500)
        return LLMRunnerOutput(raw_text=output[0]["generated_text"][-1]["content"])
