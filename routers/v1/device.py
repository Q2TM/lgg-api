from fastapi import APIRouter, Depends, Request
from schemas.device import IdentificationResp, StatusResp, Brightness
from schemas.operations import OperationResult
from schemas.shared import ChannelQueryParam
from services.lakeshore import LakeshoreService
from routers.dependencies import get_lakeshore_service

router = APIRouter(prefix="/device")


@router.post("/connect")
def connect(ls: LakeshoreService = Depends(get_lakeshore_service)) -> OperationResult:
    ls.connect()
    return OperationResult(
        is_success=True,
        message="Connected to Lakeshore Model240"
    )


@router.post("/disconnect")
def disconnect(ls: LakeshoreService = Depends(get_lakeshore_service)) -> OperationResult:
    ls.disconnect()
    return OperationResult(is_success=True, message="Disconnected from Lakeshore Model240")


@router.get("/identification", response_model=IdentificationResp)
def get_identification(ls: LakeshoreService = Depends(get_lakeshore_service)) -> IdentificationResp:
    return ls.get_identification()


@router.get("/status/{channel}", response_model=StatusResp)
def get_status(
        request: Request,
        channel: int = ChannelQueryParam,
        ls: LakeshoreService = Depends(get_lakeshore_service)) -> StatusResp:
    return ls.get_status(request, channel)

# @router.get("/id/{channel}/config")
# def set_id(channel_id=Depends(LakeshoreService.set_id)):
#     return channel_id


@router.get("/module-name")
def get_modname(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)) -> str:
    return ls.get_modname(request)


@router.put("/module-name")
def set_modname(request: Request, name: str, ls: LakeshoreService = Depends(get_lakeshore_service)) -> OperationResult:
    ls.set_modname(request, name)
    return OperationResult(is_success=True, message="Module name updated successfully")


@router.get("/brightness")
def get_brightness(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)) -> Brightness:
    return ls.get_brightness(request)


@router.put("/brightness")
def set_brightness(request: Request, brightness: int, ls: LakeshoreService = Depends(get_lakeshore_service)) -> OperationResult:
    ls.set_brightness(request, brightness)
    return OperationResult(is_success=True, message="Brightness updated successfully")


@router.delete("/factory-defaults", response_model=OperationResult)
def set_factory_defaults(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)) -> OperationResult:
    """Reset to factory defaults"""
    ls.set_factory_defaults(request)
    return OperationResult(is_success=True, message="Factory defaults restored")
