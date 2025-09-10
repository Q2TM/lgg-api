from pydantic import BaseModel, Field

class OperationResult(BaseModel):
    """Schema for the result of an operation."""

    is_success: bool = Field(...)
    message: str | None = Field(default=None)
    error: str | None = Field(default=None)
