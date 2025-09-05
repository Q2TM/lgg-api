from fastapi import APIRouter, Depends, Request, HTTPException
from schemas.reading import MonitorResp
from schemas.shared import ChannelQueryParam
from services.lakeshore import LakeshoreService
from schemas.reading import InputParameter
from routers.dependencies import get_lakeshore_service

router = APIRouter()


@router.get("/input/{channel}", response_model=InputParameter)
def get_input_parameter(
    request: Request,
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> InputParameter:
    return ls.get_input_parameter(request, channel)


@router.put("/input/{channel}")
def set_input_config(
    request: Request,
    input_param: InputParameter,
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> dict[str, str]:
    return ls.set_input_config(request, input_param, channel)


@router.get("/{channel}", response_model=MonitorResp)
def get_monitor(
    request: Request,
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> MonitorResp:
    return ls.get_monitor(request, channel)


# Missing endpoints that return 501 Not Implemented
@router.get("/sensor-units/{channel}")
def get_sensor_units_channel_reading(channel: int = ChannelQueryParam):
    """Get sensor units value - Not implemented (duplicate of get_sensor_reading)"""
    raise HTTPException(
        status_code=501, detail="Sensor units reading not implemented - use monitor endpoint instead")
