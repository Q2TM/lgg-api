from pydantic import BaseModel, Field
from typing import Optional


class OperationResult(BaseModel):
    """Schema for the result of an operation."""

    is_success: bool = Field(...)
    message: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)
