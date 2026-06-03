import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from io import BytesIO
from app import data
from app.schemas import UploadResponse


app = FastAPI(title="KK2")



@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/data/upload", response_model=UploadResponse)
async def upload_data(file: UploadFile):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Endast .csv filer accepteras.")
    
    content = await file.read()
    
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
