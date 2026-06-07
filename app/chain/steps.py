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
        prompt = f"You are a data analyst who answers questions based on the dataset's statistics. Question: {data.question} Stats: {data.stats_summary} Answer the question based on the statistics. "
    
        return PromptBuilderOutput(prompt=prompt)
    

pipe = pipeline("text-generation", model=settings.llm_name)

class LLMRunner(Runnable[PromptBuilderOutput, LLMRunnerOutput]):
    def invoke(self, data: PromptBuilderOutput) -> LLMRunnerOutput:
        messages = [
            {"role":"user", "content":data.prompt}
        ]
        output = pipe(messages, max_new_tokens=500)
        return LLMRunnerOutput(raw_text=output[0]["generated_text"][-1]["content"])

class ResponseParser(Runnable[LLMRunnerOutput, ResponseParserOutput]):
    def invoke(self, data: LLMRunnerOutput) -> ResponseParserOutput:
        answer = data.raw_text.strip()
        return ResponseParserOutput(prompt="", answer=answer)