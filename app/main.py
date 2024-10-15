from fastapi import FastAPI
from gpiozero import Device
from .api.v1.router import v1_router
from .utils.config import settings
from .utils.logger import logger
from pathlib import Path
import json

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(v1_router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": "Hello World. This is the swncrew backend"}

# Auto generate OpenAPI spec output
openapi_output_path = Path("./openapi/openapi.json")
# Ensure the output directory exists
openapi_output_path.parent.mkdir(parents=True, exist_ok=True)

# Auto generate OpenAPI spec output on startup
@app.on_event("startup")
async def generate_openapi():
    openapi = app.openapi()
    openapi_output_path.write_text(json.dumps(openapi, indent=2))
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    Device.close()