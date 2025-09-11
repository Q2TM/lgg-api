from pydantic import Field
from fastapi_camelcase import CamelModel


class IdentificationResp(CamelModel):
    """Schema for the `/id` endpoint."""

    manufacturer: str = Field(...)
    model: str = Field(...)
    serial_number: str = Field(...)
    firmware_version: str = Field(...)


class Brightness(CamelModel):
    """Schema for the brightness configuration."""

    brightness: int = Field(..., ge=0, le=100,
                            description="Brightness level between 0 and 100")


class StatusResp(CamelModel):
    """Schema for the `/{channel}/status` endpoint."""

    invalid_reading: bool = Field(...)
    temp_under_range: bool = Field(...)
    temp_over_range: bool = Field(...)
    sensor_units_over_range: bool = Field(...)
    sensor_units_under_range: bool = Field(...)
