from pydantic import BaseModel, Field
from lakeshore.model_240_enums import Model240Enums


class IdentificationResp(BaseModel):
    """Schema for the `/id` endpoint."""

    manufacturer: str = Field(..., alias="manufacturer")
    model: str = Field(..., alias="model")
    serial_number: str = Field(..., alias="serial number")
    firmware_version: str = Field(..., alias="firmware version")
    modname: str | None = Field(None, alias="modname")


class MonitorResp(BaseModel):
    """Schema for the `/monitor/{channel}` endpoint."""

    celsius: float
    fahrenheit: float
    kelvin: float
    sensor: float


class InputParameter(BaseModel):
    """Schema for the `/input/{channel}` endpoint."""

    # Optional field for sensor name, can be None if not set
    sensor_name: str | None = None
    sensor_type: Model240Enums.SensorTypes
    temperature_unit: Model240Enums.Units
    auto_range_enable: bool
    current_reversal_enable: bool
    input_enable: bool
    input_range: int
    filter: str | None = None  # Optional field for filter, can be None if not applicable


class CurveHeader(BaseModel):
    """Schema for the `/curve_header/{channel}` endpoint."""

    curve_name: str
    serial_number: str
    curve_data_format: Model240Enums.CurveFormat
    temperature_limit: float
    coefficient: Model240Enums.Coefficients


class StatusResp(BaseModel):
    """Schema for the `/status/{channel}` endpoint."""

    invalid_reading: bool = Field(..., alias="invalid reading")
    unknown: bool = Field(..., alias="")
    temp_under_range: bool = Field(..., alias="temp under range")
    temp_over_range: bool = Field(..., alias="temp over range")
    sensor_units_over_range: bool = Field(..., alias="sensor units over range")
    sensor_units_under_range: bool = Field(...,
                                           alias="sensor units under range")


class CurveDataPoint(BaseModel):
    """Schema for the curve data points."""

    temperature: float
    sensor: float


class CurveDataPoints(BaseModel):
    """Schema for the response containing multiple curve data points."""

    channel: int
    temperatures: list[float] = Field(...,
                                      description="List of temperature values")
    sensors: list[float] = Field(..., description="List of sensor values")


class Brightness(BaseModel):
    """Schema for the brightness configuration."""

    brightness: int = Field(..., ge=0, le=100,
                            description="Brightness level between 0 and 100")
