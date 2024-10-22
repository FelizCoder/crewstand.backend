from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

docs_router = APIRouter()

@docs_router.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastAPI",
        swagger_favicon_url="/static/favicon.ico"
    )
