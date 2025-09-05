from fastapi import APIRouter, Depends, Request, HTTPException
from schemas.device import IdentificationResp
from schemas.device import StatusResp
from schemas.operations import OperationResult
from schemas.shared import ChannelQueryParam
from services.lakeshore import LakeshoreService
from routers.dependencies import get_lakeshore_service

router = APIRouter()


@router.post("/connect")
def connect(ls: LakeshoreService = Depends(get_lakeshore_service)) -> OperationResult:
    result = ls.connect()

    if result:
        return OperationResult(
            is_success=result,
            message="Connected to Lakeshore Model240"
        )
    else:
        return OperationResult(is_success=False)


@router.post("/disconnect")
def disconnect(ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.disconnect()


@router.get("/identification", response_model=IdentificationResp)
def get_identification(ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.get_identification()


@router.get("/{channel}/status", response_model=StatusResp)
def get_status(
        request: Request,
        channel: int = ChannelQueryParam,
        ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_status(request, channel)

# @router.get("/id/{channel}/config")
# def set_id(channel_id=Depends(LakeshoreService.set_id)):
#     return channel_id


@router.get("/module_name")
def get_modname(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)) -> str:
    return ls.get_modname(request)


@router.put("/module_name")
def set_modname(request: Request, name: str, ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.set_modname(request, name)


@router.get("/brightness")
def get_brightness(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_brightness(request)


@router.put("/brightness")
def set_brightness(request: Request, brightness: int, ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.set_brightness(request, brightness)


# Missing endpoints that return 501 Not Implemented
@router.delete("/factory-defaults")
def set_factory_defaults():
    """Reset to factory defaults - Not implemented"""
    raise HTTPException(
        status_code=501, detail="Factory reset not implemented")
