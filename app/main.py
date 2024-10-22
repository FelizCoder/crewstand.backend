from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from .api.docs import docs_router
from .api.v1.router import v1_router
from .utils.config import settings
from .utils.logger import logger
from pathlib import Path
import json

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.VERSION,
    docs_url=None
)

app.include_router(v1_router, prefix="/v1")
# app.include_router(docs_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.PROJECT_NAME + " - Swagger UI",
        swagger_favicon_url="/favicon.ico"
    )

@app.get("/")
async def root():
    return {"message": "Hello World. This is the swncrew backend"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('/static/favicon.ico')

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
    # Close the GPIO device when the application shuts down
    settings.DEVICE.close()