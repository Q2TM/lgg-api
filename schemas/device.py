from pydantic import BaseModel, Field


class IdentificationResp(BaseModel):
    """Schema for the `/id` endpoint."""

    manufacturer: str = Field(..., alias="manufacturer")
    model: str = Field(..., alias="model")
    serial_number: str = Field(..., alias="serial number")
    firmware_version: str = Field(..., alias="firmware version")


class Brightness(BaseModel):
    """Schema for the brightness configuration."""

    brightness: int = Field(..., ge=0, le=100,
                            description="Brightness level between 0 and 100")


class StatusResp(BaseModel):
    """Schema for the `/{channel}/status` endpoint."""

    invalid_reading: bool = Field(..., alias="invalid reading")
    unknown: bool = Field(..., alias="")
    temp_under_range: bool = Field(..., alias="temp under range")
    temp_over_range: bool = Field(..., alias="temp over range")
    sensor_units_over_range: bool = Field(..., alias="sensor units over range")
    sensor_units_under_range: bool = Field(...,
                                           alias="sensor units under range")
