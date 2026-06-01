from pydantic import BaseModel

class UlpoadResponse(BaseModel):
    rows: int
    columns: int
    dtypes: dict[str, str]