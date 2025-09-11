from pydantic import Field
from fastapi_camelcase import CamelModel


class OperationResult(CamelModel):
    """Schema for the result of an operation."""

    is_success: bool = Field(...)
    message: str | None = Field(default=None)
    error: str | None = Field(default=None)
