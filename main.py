from fastapi import FastAPI
from src.controllers.uploadFile import router as upload_router

app = FastAPI()
app.include_router(upload_router)

# Test endpoint
@app.get("/")
async def getMessage():
    return {"message": "API is running"}
