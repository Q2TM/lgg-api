from fastapi import APIRouter, Depends, Request, Path
from services.lakeshore import LakeshoreService
from schemas.lakeshore import CurveHeader, CurveDataPoint, CurveDataPoints
from routers.dependencies import get_lakeshore_service

router = APIRouter(prefix="/curve")

@router.get("/header/{channel}", response_model=CurveHeader)
def get_curve_header(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_curve_header(request, channel)

@router.put("/header/{channel}/config")
def set_curve_header(request: Request, curve_header: CurveHeader, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.set_curve_header(request, channel, curve_header)

@router.get("/data-point/{channel}/{index}", response_model=CurveDataPoint)
def get_curve_data_point(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), index: int = Path(..., ge=1, le=200, description="Index of the data point in the curve"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_curve_data_point(request, channel, index)

@router.get("/curve_data_points/{channel}/all", response_model=CurveDataPoints)
def get_curve_data_points(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.get_curve_data_points(request, channel)

@router.put("/data-point/{channel}/{index}", response_model=CurveDataPoint)
async def set_curve_data_point(request: Request, data_point: CurveDataPoint, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), index: int = Path(..., ge=1, le=200, description="Index of the data point in the curve"),  ls: LakeshoreService = Depends(get_lakeshore_service)):
    return ls.set_curve_data_point(request, channel, index, data_point)
