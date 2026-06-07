import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from io import BytesIO
from app import data
from app.schemas import UploadResponse, StatsResponse, AskRequest, AskResponse
from app.chain.pipeline import oraklet
from app.chain.steps import PromptBuilderInput
from app.config import settings


app = FastAPI(title="KK2")



@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/data/upload", response_model=UploadResponse)
async def upload_data(file: UploadFile):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Endast .csv filer accepteras.")
    
    content = await file.read()
    
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail=f"Filen är för stor. Max tillåtna storleken är {settings.max_file_size_mb} MB.")

    try:
        df = pd.read_csv(BytesIO(content))
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise HTTPException(status_code=400, detail=f"Kunde inte läsa CSV {e}")
    
    data.dataset = df
    

    return UploadResponse(
        rows=len(df),
        columns=df.columns.tolist(),
        dtypes=df.dtypes.astype(str).to_dict()
    )


@app.get("/data/stats", response_model=StatsResponse)
def get_stats():
    if data.dataset is None:
        raise HTTPException(status_code=404, detail="Inget dataset har laddats upp ännu.")
    
    return StatsResponse(stats=data.dataset.describe().to_dict())



@app.post("/ai/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if data.dataset is None:
        raise HTTPException(status_code=404, detail="Inget dataset har laddats upp ännu.")
    try:
        result = oraklet.invoke(PromptBuilderInput(question=request.question, stats_summary=data.dataset.describe().to_string()))
        return AskResponse(question=request.question, answer = result.answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ett fel inträffade: {e}")