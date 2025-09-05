from fastapi import APIRouter, Depends, HTTPException, Request
from schemas.curve import CurveDataPoint, CurveHeader, IndexQueryParam
from schemas.shared import ChannelQueryParam
from services.lakeshore import LakeshoreService
from schemas.curve import CurveDataPoints
from routers.dependencies import get_lakeshore_service

router = APIRouter(prefix="/curve")


@router.get("/{channel}/header", response_model=CurveHeader)
def get_curve_header(
    request: Request,
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> CurveHeader:
    return ls.get_curve_header(request, channel)


@router.put("/{channel}/header")
def set_curve_header(
    request: Request,
    curve_header: CurveHeader,
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> dict[str, str]:
    return ls.set_curve_header(request, curve_header, channel)


@router.get("/{channel}/data-point/{index}", response_model=CurveDataPoint)
def get_curve_data_point(
    request: Request,
    channel: int = ChannelQueryParam,
    index: int = IndexQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> CurveDataPoint:
    return ls.get_curve_data_point(request, channel, index)


@router.get("/{channel}/data-points", response_model=CurveDataPoints)
def get_curve_data_points(
    request: Request,
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> CurveDataPoints:
    return ls.get_curve_data_points(request, channel)


@router.put("/{channel}/data-point/{index}")
async def set_curve_data_point(
    request: Request,
    data_point: CurveDataPoint,
    channel: int = ChannelQueryParam,
    index: int = IndexQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> dict[str, str]:
    return ls.set_curve_data_point(request, data_point, channel, index)


@router.delete("/{channel}")
def delete_curve(
    channel: int = ChannelQueryParam,
    ls: LakeshoreService = Depends(get_lakeshore_service)
) -> dict[str, str]:
    """Delete user curve - Not implemented"""
    raise HTTPException(status_code=501, detail="Delete curve not implemented")
