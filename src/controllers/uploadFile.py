from fastapi import UploadFile, File, APIRouter
from ..services.uploadFileService import uploadFileService

router = APIRouter(prefix="", tags=["Upload"])

@router.post("/load")
async def upload_file(file: UploadFile = File(...)):
    
    if not (file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
        return {
            "error": "Formato no soportado",
            "message": "Por favor, suba un archivo Excel con extensión .xls o .xlsx",
            "status_code": 400
        }
    
    try:
        await uploadFileService(file)
        return {
            "status_code": 200,
            "message": "Datos cargados correctamente",
        }

    except ValueError as e:
        return {
            "status_code": 400,
            "message": f"Error en los datos: {str(e)}"
        }

    except Exception as e:
        return {
            "status_code": 500,
            "message": f"Error interno del servidor: {str(e)}"
        }