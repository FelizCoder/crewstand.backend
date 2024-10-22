"""
This module contains the FastAPI application for the swncrew backend.
"""

from pathlib import Path
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from .api.v1.router import v1_router
from .utils.config import settings
from .utils.logger import logger

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, docs_url=None)

app.include_router(v1_router, prefix="/v1")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    """
    Serve the Swagger UI HTML page for API documentation.

    Returns:
        HTMLResponse: The Swagger UI as an HTML page.
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.PROJECT_NAME + " - Swagger UI",
        swagger_favicon_url="/favicon.ico",
    )


@app.get("/")
async def root():
    """
    Returns a simple greeting message.

    Returns:
        dict: A dictionary containing a single key-value pair with the message.
    """
    return {"message": "Hello World. This is the swncrew backend"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    This endpoint is used to serve the favicon.ico file.

    Returns:
        FileResponse: The favicon.ico file.
    """
    return FileResponse("app/static/favicon.ico")


# Auto generate OpenAPI spec output
openapi_output_path = Path("./openapi/openapi.json")
# Ensure the output directory exists
openapi_output_path.parent.mkdir(parents=True, exist_ok=True)


# Auto generate OpenAPI spec output on startup
@app.on_event("startup")
async def generate_openapi():
    """
    Generates the OpenAPI specification and saves it to a file on startup.
    """
    openapi = app.openapi()
    openapi_output_path.write_text(json.dumps(openapi, indent=2), encoding="utf-8")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Logs a shutdown message when the application is shutting down.
    Close the GPIO device when the application shuts down
    """
    logger.info("Shutting down...")
    # Close the GPIO device when the application shuts down
    settings.DEVICE.close()
