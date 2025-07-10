from fastapi import FastAPI, Depends, HTTPException, Request, Path
from contextlib import asynccontextmanager
from lakeshore import Model240, Model240InputParameter, Model240CurveHeader
import asyncio

from model import IdentificationResp, MonitorResp, InputParameter, CurveHeader, StatusResp, CurveDataPoint, Brightness, CurveDataPoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.module = None
    app.state.lock = asyncio.Lock()
    yield
    mod = getattr(app.state, "module", None)
    if mod:
        try:
            mod.disconnect_usb()
        except Exception:
            pass

app = FastAPI(title="Lakeshore Model240 API",
              description="API for Lakeshore Model240 temperature controller",
              version="1.0.0",
              lifespan=lifespan)


def get_module(request: Request) -> Model240:
    module = getattr(request.app.state, "module", None)
    if module is None:
        raise HTTPException(503, "Model240 not connected")
    return module


@app.get("/")
async def root():
    return {"message": "Hello World"}


# GET methods for Model240----------------------------------------------------------------------------

@app.get("/id", response_model=IdentificationResp)
async def get_id(request: Request, device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        return device.get_identification()


@app.get("/input/{channel}", response_model=InputParameter)
async def get_inputparameter(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        input_param = device.get_input_parameter(channel).__dict__
        return {'sensor_name': device.get_sensor_name(channel),
                **input_param,
                'filter': device.get_filter(channel)}


@app.get("/curve_header/{channel}", response_model=CurveHeader)
async def get_curve_header(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        return device.get_curve_header(channel).__dict__


@app.get("/monitor/{channel}", response_model=MonitorResp)
async def get_monitor(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        celsius = device.get_celsius_reading(channel)
        farenheit = device.get_fahrenheit_reading(channel)
        kelvin = device.get_kelvin_reading(channel)
        sensor = device.get_sensor_reading(channel)
        return {'celsius': celsius,
                'fahrenheit': farenheit,
                'kelvin': kelvin,
                'sensor': sensor}


@app.get("/status/{channel}", response_model=StatusResp)
async def get_status(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        return device.get_channel_reading_status(channel)


@app.get("/curve_data_point/{channel}/{index}", response_model=CurveDataPoint)
async def get_curve_data_point(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), index: int = Path(..., ge=1, le=200, description="Index of the data point in the curve"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        sensor, temp = device.get_curve_data_point(channel, index).split(',')
        return CurveDataPoint(
            temperature=float(temp),
            sensor=float(sensor)
        )


@app.get("/curve_data_points/{channel}/all", response_model=CurveDataPoints)
async def get_curve_data_points_all(request: Request, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        raw_data = [device.get_curve_data_point(
            channel, i).split(',') for i in range(1, 201)]
        sensors = [dp[0] for dp in raw_data]
        temperatures = [dp[1] for dp in raw_data]
        return CurveDataPoints(
            channel=channel,
            temperatures=temperatures,
            sensors=sensors
        )


# For Brghtness, the model240 method doesn't work

# @app.get("/brightness")
# async def get_brightness(request: Request, device: Model240 = Depends(get_module)):
#     async with request.app.state.lock:
#         try:
#             brightness = device.get_brightness()
#         except Exception as e:
#             print("Faile to get :", e)
#         return {"brightness": brightness}


# POST methods for Model240----------------------------------------------------------------------------

@app.put("/connect")
async def connect(request: Request):
    if request.app.state.module is None:
        try:
            request.app.state.module = Model240()
        except Exception as e:
            raise HTTPException(503, f"Connect failed: {e}")
    return {"message": "Connected"}


@app.put("/disconnect")
async def disconnect(request: Request):
    module = getattr(request.app.state, "module", None)
    if module is not None:
        module.disconnect_usb()
        request.app.state.module = None
    return {"message": "Disconnected"}


@app.put("/input/{channel}/config")
async def set_input_config(request: Request, input_param: InputParameter, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        try:
            inp: Model240InputParameter = Model240InputParameter(
                sensor=input_param.sensor_type,
                auto_range_enable=input_param.auto_range_enable,
                current_reversal_enable=input_param.current_reversal_enable,
                units=input_param.temperature_unit,
                input_enable=input_param.input_enable,
                input_range=input_param.input_range
            )
            device.set_input_parameter(channel, inp)
            if input_param.filter is not None:
                device.set_filter(channel, input_param.filter)
            if input_param.sensor_name is not None:
                device.set_sensor_name(channel, input_param.sensor_name)
            return {"message": "Input configuration updated"}
        except Exception as e:
            raise HTTPException(503, f"Update failed: {e}")


@app.put("/curve_header/{channel}/config")
async def set_curve_header(request: Request, curve_header: CurveHeader, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        try:
            curve_header_resp = Model240CurveHeader(
                curve_name=curve_header.curve_name,
                serial_number=curve_header.serial_number,
                curve_data_format=curve_header.curve_data_format,
                temperature_limit=curve_header.temperature_limit,
                coefficient=curve_header.coefficient
            )
            device.set_curve_header(channel, curve_header_resp)
            return {"message": "Curve header updated"}
        except Exception as e:
            raise HTTPException(503, f"Update failed: {e}")


@app.put("/id/{channel}/config")
async def set_id(request: Request, modname: str,  channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        try:
            device.set_modname(modname)
            return {"message": "Modname updated"}
        except Exception as e:
            raise HTTPException(503, f"Update failed: {e}")


@app.put("/brightness/config")
async def set_brightness(request: Request, brightness: Brightness, device: Model240 = Depends(get_module)):
    if brightness < 0 or brightness > 100:
        raise HTTPException(400, "Brightness must be between 0 and 100")
    async with request.app.state.lock:
        try:
            device.set_brightness(brightness)
            return {"message": "Brightness updated"}
        except Exception as e:
            raise HTTPException(503, f"Update failed: {e}")


@app.put("/curve_data_point/{channel}/{index}")
async def set_curve_data_point(request: Request, data_point: CurveDataPoint, channel: int = Path(..., ge=1, le=8, description="Channel must be between 1 and 8"), index: int = Path(..., ge=1, le=200, description="Index of the data point in the curve"), device: Model240 = Depends(get_module)):
    async with request.app.state.lock:
        try:
            device.set_curve_data_point(
                channel, index, data_point.sensor, data_point.temperature)
            return {"message": "Curve data point updated"}
        except Exception as e:
            raise HTTPException(503, f"Update failed: {e}")
