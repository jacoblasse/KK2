from typing import Any, Callable, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, SerializeAsAny

I = TypeVar("I")
O = TypeVar("O")

class Runnable(BaseModel, Generic[I, O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None

    def invoke(self, data: I) -> O:
        raise NotImplementedError("Subclasses must implement the invoke method.")
    
    def __or__(self, other: Any) -> "RunnableSequence":
        if isinstance(other, Runnable):
            return RunnableSequence.model_construct(first =self, second=other)
        if callable(other):
            return RunnableSequence.model_construct(first =self, second=RunnableLambda(func=other))
        return NotImplemented
    
    def __ror__(self, other: Any) -> "RunnableSequence":
            if callable(other):
                return RunnableSequence.model_construct(
                    first=RunnableLambda.model_construct(func=other),
                    second=self,
                )
            return NotImplemented
    
class RunnableLambda(Runnable[I, O]):
    func: Callable[[I], O]

    def invoke(self, data: I) -> O:
        return self.func(data)
    


class RunnableSequence(Runnable[I, O], Generic[I, O]):
    first: SerializeAsAny[Runnable]
    second: SerializeAsAny[Runnable]

    def invoke(self, data: I) -> O:
        return self.second.invoke(self.first.invoke(data))