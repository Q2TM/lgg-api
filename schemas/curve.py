from fastapi import Path
from lakeshore.model_240_enums import Model240Enums
from pydantic import Field
from fastapi_camelcase import CamelModel


class CurveHeader(CamelModel):
    """Schema for the `/curve/{channel}/header` endpoint."""

    curve_name: str
    serial_number: str
    curve_data_format: Model240Enums.CurveFormat
    temperature_limit: float
    coefficient: Model240Enums.Coefficients


class CurveDataPoint(CamelModel):
    """Schema for the curve data points."""

    temperature: float
    sensor: float


class CurveDataPoints(CamelModel):
    """Schema for the response containing multiple curve data points."""

    channel: int
    temperatures: list[float] = Field(
        ...,
        description="List of temperature values")
    sensors: list[float] = Field(..., description="List of sensor values")


IndexQueryParam = Path(
    ..., ge=1, le=200, description="Index of the data point in the curve")
