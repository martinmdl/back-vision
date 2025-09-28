from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/train")
async def train_endpoint(file: UploadFile = File(...)):
    # Leer dataset
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith(".xls") or file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        return {"error": "Formato no soportado"}

    return {
        "status": "ok",
    }