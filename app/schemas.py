from pydantic import BaseModel

class UploadResponse(BaseModel):
    rows: int
    columns: int
    dtypes: dict[str, str]