from fastapi import UploadFile, File, APIRouter
from src.services.cleanDataService import clean_xls
from src.services.dbService import save_to_postgres
# from utils.weather import getWeather

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/load")
async def upload_file(file: UploadFile = File(...)):
    
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

    # clima (consultar API: https://data.meteostat.net/daily/2025/87585.csv.gz )
    # df_clima = getWeather()

    # feriados (buscar API)

    # unificar_coso

    # entrenar_modelo

    return {
        "status_code": 200,
        "message": "Datos cargados correctamente"
    }