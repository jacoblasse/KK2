from typing import Any, Callable, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, SerializeAsAny

I = TypeVar("I")
O = TypeVar("O")

class Runnable(BaseModel, Generic[I, O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None

    def invoke(self, data: I) -> O:
        raise NotImplementedError("Subclasses must implement the invoke method.")