from fastapi import APIRouter, Depends, Request, Path
from services.lakeshore import LakeshoreService
from schemas.lakeshore import MonitorResp, InputParameter
from routers.dependencies import get_lakeshore_service

router = APIRouter()


@router.get("/input/{channel}", response_model=InputParameter)
def get_input_parameter(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_input_parameter(request=request, channel=channel)

@router.put("/input/{channel}/config")
def set_input_config(request: Request, input_param: InputParameter, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.set_input_config(request=request, input_param=input_param, channel=channel)


@router.get("/{channel}", response_model=MonitorResp)
def get_monitor(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_monitor(request=request, channel=channel)
