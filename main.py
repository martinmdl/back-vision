from fastapi import FastAPI
from src.controllers.uploadFile import router as upload_router
from src.utils.weather import getWeather

app = FastAPI()
app.include_router(upload_router)

# Test endpoint
@app.get("/")
async def getMessage():
    return {"message": "API is running"}

@app.get("/weather")
async def getWeatherAPI():
    await getWeather()
    return {"status": "success"}