from lakeshore.model_240_enums import Model240Enums
from fastapi_camelcase import CamelModel


class MonitorResp(CamelModel):
    """Schema for the `/{channel}` endpoint."""

    # celsius: float
    # fahrenheit: float
    kelvin: float
    sensor: float


class InputParameter(CamelModel):
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
