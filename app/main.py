import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
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
    
    try:
        df = pd.read_csv(file.file)
    except (pd.errors.Parsererror, UnicodeDecodeError) as e:
        raise HTTPException(status_code=400, detail=f"Kunde inte läsa CSV {e}")
    

    return UploadResponse(
        rows=len(df),
        columns=df.columns.tolist(),
        dtypes=df.dtypes.astype(str).to_dict()
    )
