from fastapi import APIRouter
from app.utils.config import settings


router = APIRouter()


@router.get("/version", response_model=str)
def get_version():
    """
    **Summary**

    Retrieves the current version information of the application.

    **Parameters**

    None

    **Returns**

    str
        The version information of the application, as defined in `settings.VERSION`.

    **Notes**

    This endpoint provides a simple way to determine the version of the API.
    The version information is sourced from the application's settings.

    **Examples**

    >>> response = get_version()
    >>> print(response)
    # Output: <current_version_string> (e.g., "1.2.3")

    """

    info = settings.VERSION
    return info
