from fastapi import APIRouter, Depends, Request, Path
from schemas.lakeshore import IdentificationResp, StatusResp
from services.lakeshore import LakeshoreService
from routers.dependencies import get_lakeshore_service

router = APIRouter()


@router.post("/connect")
def connect(ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.connect()


@router.post("/disconnect")
def disconnect(ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.disconnect()


@router.get("/identification", response_model=IdentificationResp)
def get_identification(ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.get_identification()


@router.get("/{channel}/status", response_model=StatusResp)
def get_status(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"),  ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_status(request, channel)

# @router.get("/id/{channel}/config")
# def set_id(channel_id=Depends(LakeshoreService.set_id)):
#     return channel_id


@router.get("/module_name")
def get_modname(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)) -> str:
    return ls.get_modname(request)


@router.post("/module_name")
def set_modname(request: Request, name: str, ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.set_modname(request, name)


@router.get("/brightness")
def get_brightness(request: Request, ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_brightness(request)


@router.post("/brightness")
def set_brightness(request: Request, brightness: int, ls: LakeshoreService = Depends(get_lakeshore_service)) -> dict[str, str]:
    return ls.set_brightness(request, brightness)
