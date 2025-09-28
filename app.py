from fastapi import FastAPI, UploadFile, File
from service.cleaning import clean

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#### Controllers ####

@app.post("/load")
async def train_endpoint(file: UploadFile = File(...)):
    
    if not (file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
        return {
            "error": "Formato no soportado",
            "message": "Por favor, suba un archivo Excel con extensión .xls o .xlsx",
            "status_code": 400
        }
    
    df_clean = clean(file.file)

    return {
        "status_code": 200,
        "df_clean": df_clean.to_dict(orient="records")
    }