from fastapi import APIRouter
from ..services.predictSalesService import predecir_7_dias

router = APIRouter(prefix="", tags=["Predict"])

@router.post("/predict")

async def predict():
    predicciones = await predecir_7_dias()
    return predicciones.to_dict(orient="records")