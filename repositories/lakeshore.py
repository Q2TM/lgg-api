from lakeshore import Model240, Model240InputParameter, Model240CurveHeader
from contextlib import asynccontextmanager
from threading import Lock
from fastapi import FastAPI


from schemas.lakeshore import CurveDataPoint, InputParameter, MonitorResp, CurveDataPoints, CurveHeader
from exceptions.lakeshore import DeviceNotConnectedError, ChannelError


class LakeshoreRepository:
    device: Model240 | None = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of LakeshoreService exists."""
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def connect():
        """Connect to the Model240 device."""
        if LakeshoreRepository.device is None:
            LakeshoreRepository.device = Model240()

    @staticmethod
    def disconnect():
        """Disconnect from the Model240 device."""
        if LakeshoreRepository.device:
            print("Disconnecting Model240")
            LakeshoreRepository.device.disconnect_usb()
            LakeshoreRepository.device = None
        print("Device disconnected")

    @asynccontextmanager
    @staticmethod
    async def lifespan(app: FastAPI):
        """Lifespan context manager to handle application startup and shutdown."""
        app.state.lock = Lock()
        yield
        LakeshoreRepository.disconnect()

    @staticmethod
    def get_device():
        if not LakeshoreRepository.device:
            raise DeviceNotConnectedError()
        return LakeshoreRepository.device

    def get_status(self, channel: int):
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        return device.get_channel_reading_status(channel)

    def get_identification(self):
        device = self.get_device()
        return device.get_identification()

    def get_input_parameter(self, channel: int) -> InputParameter:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        input_param = device.get_input_parameter(channel).__dict__
        print(input_param)
        return InputParameter(sensor_name=device.get_sensor_name(channel), **input_param, filter=device.get_filter(channel))

    def set_modname(self, modname: str):
        device = self.get_device()
        device.set_modname(modname)

    def set_brightness(self, brightness: int):
        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")
        device = self.get_device()
        device.set_brightness(brightness)

    def set_input_config(self, input_param: InputParameter, channel: int):
        device = self.get_device()
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

    def get_monitor(self, channel: int) -> MonitorResp:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        celsius = device.get_celsius_reading(channel)
        farenheit = device.get_fahrenheit_reading(channel)
        kelvin = device.get_kelvin_reading(channel)
        sensor = device.get_sensor_reading(channel)
        return MonitorResp(
            celsius=float(celsius),
            fahrenheit=float(farenheit),
            kelvin=kelvin,
            sensor=sensor
        )

    def get_curve_header(self, channel: int) -> CurveHeader:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        return CurveHeader(**device.get_curve_header(channel).__dict__)

    def get_curve_data_point(self, channel: int, index: int) -> CurveDataPoint:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        sensor, temp = str(device.get_curve_data_point(
            channel, index)).split(',')
        return CurveDataPoint(
            temperature=float(temp),
            sensor=float(sensor)
        )

    def get_curve_data_points(self, channel: int) -> CurveDataPoints:
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        raw_data = [device.get_curve_data_point(
            channel, i).split(',') for i in range(1, 201)]
        sensors = [dp[0] for dp in raw_data]
        temperatures = [dp[1] for dp in raw_data]
        return CurveDataPoints(
            channel=channel,
            temperatures=list(map(float, temperatures)),
            sensors=list(map(float, sensors))
        )

    def set_curve_header(self, curve_header: CurveHeader, channel: int):
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
        device.set_curve_header(channel, curve_header_resp)

    def set_curve_data_point(self, data_point: CurveDataPoint, channel: int, index: int):
        if not 1 <= channel <= 8:
            raise ChannelError(channel)
        device = self.get_device()
        device.set_curve_data_point(
            channel, index, data_point.sensor, data_point.temperature)
