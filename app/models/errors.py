from typing import List, Optional, Union
from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    """
    A model representing a validation error, detailing the specific issue encountered.
    """

    loc: List[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")
    input: Optional[str | int] = Field(..., title="Input")


class HTTPValidationError(BaseModel):
    """
    A model representing an HTTP validation error, which may contain multiple `ValidationError` instances.
    """

    detail: Optional[List[ValidationError]] = Field(None, title="Detail")
