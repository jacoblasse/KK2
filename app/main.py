from fastapi import FastAPI, UploadFile, HTTPException
from app import data
from app.schemas import UploadResponse


app = FastAPI(title="KK2")



@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/data/upload", response_model=UploadResponse)
async def upload_data(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Endast .csv filer accepteras.")
    
    raise HTTPException(status_code=501, detail="inte implementerat än")