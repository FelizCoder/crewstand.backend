from fastapi import FastAPI
from .api.v1.router import v1_router

app = FastAPI(title="swncrew backend")

app.include_router(v1_router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": "Hello World. This is the swncrew backend"}