from fastapi import FastAPI
from .api.v1.router import v1_router
from .utils.config import config
from pathlib import Path
import json

app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

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