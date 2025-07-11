from fastapi import APIRouter, Depends, Request, Path
from schemas.lakeshore import IdentificationResp, StatusResp
from services.lakeshore import LakeshoreService
from routers.dependencies import get_lakeshore_service

router = APIRouter()

@router.put("/connect")
def connect(ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.connect()

@router.put("/disconnect")
def disconnect(ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.disconnect()

@router.get("/id", response_model=IdentificationResp)
def get_id(ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_identification()

@router.get("/status/{channel}", response_model=StatusResp)
def get_status(request: Request, channel: int  = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"),  ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_status(request, channel)

# @router.get("/id/{channel}/config")
# def set_id(channel_id=Depends(LakeshoreService.set_id)):
#     return channel_id

@router.put("/id/config")
def set_modname(request: Request, name: str, ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.set_modname(request, name)

@router.put("/brightness/config")
def set_brightness(request: Request, brightness: int, ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.set_brightness(request, brightness)
