from fastapi import FastAPI, UploadFile, File
from src.services.cleanDataService import clean_xls
from src.services.dbService import save_to_postgres

app = FastAPI()

#### Controllers ####
@app.post("/load")
async def train_endpoint(file: UploadFile = File(...)):
    
    # Validación de extensión
    if not (file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
        return {
            "error": "Formato no soportado",
            "message": "Por favor, suba un archivo Excel con extensión .xls o .xlsx",
            "status_code": 400
        }
    
    # Limpieza de datos y obtención de DataFrames
    df_venta, df_producto, df_detalle_venta = clean_xls(file.file)
    
    # Guardar en la base de datos (upsert para no duplicar)
    save_to_postgres(df_venta, df_producto, df_detalle_venta)

    return {
        "status_code": 200,
        "message": "Datos cargados correctamente"
    }