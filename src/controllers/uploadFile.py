from fastapi import UploadFile, File, APIRouter
from ..services.cleanBusinessData import clean_xls
from ..services.updateDB import save_to_postgres
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
    
    # clima (consultar API: https://data.meteostat.net/daily/<AÑOS>/87585.csv.gz)
    df_clima_api = await getWeather(df_venta)
    df_clima = cleanWeather(df_clima_api)

    # Guardar en la base de datos (upsert para no duplicar)
    save_to_postgres(df_venta, "ventas", "idVenta")
    save_to_postgres(df_producto, "productos", "idProducto")
    save_to_postgres(df_detalle_venta, "detalle_ventas", "idDetalle")
    ### TODO guardar df_clima en la base de datos ###
    save_to_postgres(df_clima, "clima", "fecha")


    # feriados (buscar API)

    # unificar_coso

    # entrenar_modelo

    return {
        "status_code": 200,
        "message": "Datos cargados correctamente"
    }