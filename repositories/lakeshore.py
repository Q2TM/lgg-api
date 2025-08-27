from contextlib import asynccontextmanager
from threading import Lock
from fastapi import FastAPI
from lakeshore import Model240, Model240InputParameter, Model240CurveHeader
import os

from constants.env import USE_MOCK
from mocks.model240 import MockModel240

from typing import Self, cast
from collections.abc import AsyncGenerator
from schemas.lakeshore import CurveDataPoint, InputParameter, MonitorResp, CurveDataPoints, CurveHeader
from exceptions.lakeshore import DeviceNotConnectedError, ChannelError


class LakeshoreRepository:
    device: Model240 | None = None

    def __new__(cls) -> Self:
        """Singleton pattern to ensure only one instance of LakeshoreService exists."""
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def connect() -> bool:
        """Connect to the Model240 device."""
        if LakeshoreRepository.device is None:
            if os.getenv(USE_MOCK):
                print("Using MockModel240")
                LakeshoreRepository.device = MockModel240()  # type: ignore
            else:
                LakeshoreRepository.device = Model240()
            return True

        return False

    @staticmethod
    def disconnect() -> None:
        """Disconnect from the Model240 device."""
        if LakeshoreRepository.device:
            print("Disconnecting Model240")
            LakeshoreRepository.device.disconnect_usb()
            LakeshoreRepository.device = None
        print("Device disconnected")

    @asynccontextmanager
    @staticmethod
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Lifespan context manager to handle application startup and shutdown."""
        app.state.lock = Lock()
        yield
        LakeshoreRepository.disconnect()

    @staticmethod
    def get_device() -> Model240:
        if not LakeshoreRepository.device:
            raise DeviceNotConnectedError()
        return LakeshoreRepository.device

    def get_status(self, channel: int) -> dict[str, str]:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        return device.get_channel_reading_status(channel)  # type: ignore

    def get_identification(self) -> dict[str, str]:
        device = self.get_device()
        return device.get_identification()  # type: ignore

    def get_input_parameter(self, channel: int) -> InputParameter:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        input_param = device.get_input_parameter(
            channel).__dict__  # type: ignore
        print(input_param)
        # type: ignore
        return InputParameter(sensor_name=device.get_sensor_name(channel), **input_param, filter=device.get_filter(channel))

    def get_modname(self) -> str:
        device = self.get_device()
        return device.get_modname()

    def set_modname(self, modname: str) -> None:
        device = self.get_device()
        device.set_modname(modname)

    def get_brightness(self) -> int:
        device = self.get_device()
        brightness = int(device.query("BRIGT?"))
        if brightness == 0:
            return 0
        if brightness == 1:
            return 25
        if brightness == 2:
            return 50
        if brightness == 3:
            return 75
        if brightness == 4:
            return 100
        raise ValueError("Invalid brightness level")

    def set_brightness(self, brightness: int) -> None:
        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")
        device = self.get_device()
        device.set_brightness(brightness)  # type: ignore

    def set_input_config(self, input_param: InputParameter, channel: int) -> None:
        device = self.get_device()
        inp: Model240InputParameter = Model240InputParameter(
            sensor=input_param.sensor_type,
            auto_range_enable=input_param.auto_range_enable,
            current_reversal_enable=input_param.current_reversal_enable,
            units=input_param.temperature_unit,
            input_enable=input_param.input_enable,
            input_range=input_param.input_range
        )
        device.set_input_parameter(channel, inp)  # type: ignore
        if input_param.filter is not None:
            device.set_filter(channel, input_param.filter)  # type: ignore
        if input_param.sensor_name is not None:
            device.set_sensor_name(
                channel, input_param.sensor_name)  # type: ignore

    def get_monitor(self, channel: int) -> MonitorResp:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        celsius = device.get_celsius_reading(channel)  # type: ignore
        farenheit = device.get_fahrenheit_reading(channel)  # type: ignore
        kelvin = device.get_kelvin_reading(channel)  # type: ignore
        sensor = device.get_sensor_reading(channel)  # type: ignore
        return MonitorResp(
            celsius=cast(float, celsius),
            fahrenheit=cast(float, farenheit),
            kelvin=kelvin,
            sensor=sensor
        )

    def get_curve_header(self, channel: int) -> CurveHeader:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        # type: ignore
        return CurveHeader(**device.get_curve_header(channel).__dict__)

    def get_curve_data_point(self, channel: int, index: int) -> CurveDataPoint:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        sensor, temp = str(device.get_curve_data_point(  # type: ignore
            channel, index)).split(',')
        return CurveDataPoint(
            temperature=float(temp),
            sensor=float(sensor)
        )

    def get_curve_data_points(self, channel: int) -> CurveDataPoints:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        raw_data: str = [device.get_curve_data_point(  # type: ignore
            channel, i).split(',') for i in range(1, 201)]
        sensors = [dp[0] for dp in raw_data]
        temperatures = [dp[1] for dp in raw_data]
        return CurveDataPoints(
            channel=channel,
            temperatures=list(map(float, temperatures)),
            sensors=list(map(float, sensors))
        )

    def set_curve_header(self, curve_header: CurveHeader, channel: int) -> None:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        curve_header_resp = Model240CurveHeader(
            curve_name=curve_header.curve_name,
            serial_number=curve_header.serial_number,
            curve_data_format=curve_header.curve_data_format,
            temperature_limit=curve_header.temperature_limit,
            coefficient=curve_header.coefficient
        )
        device.set_curve_header(channel, curve_header_resp)  # type: ignore

    def set_curve_data_point(self, data_point: CurveDataPoint, channel: int, index: int) -> None:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        device.set_curve_data_point(  # type: ignore
            channel, index, data_point.sensor, data_point.temperature)
