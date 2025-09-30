from fastapi import FastAPI, UploadFile, File
from src.services.trainService import clean

app = FastAPI()

#### Controllers ####

@app.post("/load")
async def train_endpoint(file: UploadFile = File(...)):
    
    if not (file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
        return {
            "error": "Formato no soportado",
            "message": "Por favor, suba un archivo Excel con extensión .xls o .xlsx",
            "status_code": 400
        }
    
    clean(file.file)

    return {
        "status_code": 200,
    }