from fastapi import APIRouter, Depends, Request, Path, HTTPException
from services.lakeshore import LakeshoreService
from schemas.lakeshore import MonitorResp, InputParameter
from routers.dependencies import get_lakeshore_service

router = APIRouter()


@router.get("/input/{channel}", response_model=InputParameter)
def get_input_parameter(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)) -> InputParameter:
    return ls.get_input_parameter(request, channel)


@router.put("/input/{channel}")
def set_input_config(request: Request, input_param: InputParameter, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.set_input_config(request, input_param, channel)


@router.get("/{channel}", response_model=MonitorResp)
def get_monitor(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)) -> MonitorResp:
    return ls.get_monitor(request, channel)


# Missing endpoints that return 501 Not Implemented
@router.get("/sensor-units/{channel}")
def get_sensor_units_channel_reading(channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8")):
    """Get sensor units value - Not implemented (duplicate of get_sensor_reading)"""
    raise HTTPException(
        status_code=501, detail="Sensor units reading not implemented - use monitor endpoint instead")
