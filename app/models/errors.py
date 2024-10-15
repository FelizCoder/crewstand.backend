from typing import List, Optional, Union
from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    loc: List[Union[str, int]] = Field(..., title='Location')
    msg: str = Field(..., title='Message')
    type: str = Field(..., title='Error Type')
    input: Optional[str | int] = Field(..., title='Input')


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title='Detail')
