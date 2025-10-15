from fastapi import UploadFile, File, APIRouter
import pandas as pd
from ..utils.holiday import buildTypesCatalog, cleanHolidays, getHoliday
from ..services.cleanBusinessData import clean_xls
from ..db.updateDB import save_to_postgres
from ..services.cleanWeatherData import cleanWeather
from ..utils.weather import getWeather

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
    save_to_postgres(df_venta, "ventas", "id_venta")
    save_to_postgres(df_producto, "productos", "id_producto")
    save_to_postgres(df_detalle_venta, "detalle_ventas", "id_detalle")

    # clima (consultar API: https://data.meteostat.net/daily/<AÑOS>/87585.csv.gz)
    df_clima_api = await getWeather(df_venta)
    df_clima = cleanWeather(df_clima_api)
    save_to_postgres(df_clima, "clima", "fecha")

    # feriados (consultar API: https://api.argentinadatos.com/v1/feriados/<AÑOS>)
    df_feriado, df_catalog = await getHoliday(df_venta)
    save_to_postgres(df_catalog, "tipo_feriado", "id_tipo_feriado") 
    save_to_postgres(df_feriado, "feriado", "id_feriado")

    # ver donde va la creacion de venta_feriado
    df_venta["fecha_venta"] = pd.to_datetime(df_venta["creacion"]).dt.normalize()
    df_feriado["fecha_feriado"] = pd.to_datetime(df_feriado["fecha"]).dt.normalize()
    df_venta_feriado = df_venta.merge(df_feriado, left_on="fecha_venta", right_on="fecha_feriado", how="inner")
    df_venta_feriado = df_venta_feriado[["id_venta", "id_feriado"]]
    df_venta_feriado["id_venta_feriado"] = range(1, len(df_venta_feriado)+1)
    save_to_postgres(df_venta_feriado, "venta_feriado", "id_venta_feriado")

    # unificar_coso

    # entrenar_modelo

    return {
        "status_code": 200,
        "message": "Datos cargados correctamente"
    }