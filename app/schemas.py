from pydantic import BaseModel

class UploadResponse(BaseModel):
    rows: int
    columns: list[str]
    dtypes: dict[str, str]



class StatsResponse(BaseModel):
    stats: dict[str, dict[str, float]]