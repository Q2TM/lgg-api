from fastapi import HTTPException, Path, Request
from repositories.lakeshore import LakeshoreRepository 
from schemas.lakeshore import CurveDataPoint, InputParameter, MonitorResp, CurveDataPoints, CurveHeader


class LakeshoreService:
    __slots__ = ('ls_repo')
    
    def __new__(cls):
        """Singleton pattern, only one instance of LakeshoreService exists."""
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the LakeshoreService with a repository instance."""
        if not hasattr(self, 'ls_repo'):
            self.ls_repo = LakeshoreRepository()

    def connect(self):
        try:       
            self.ls_repo.connect()
        except Exception as e:
            raise HTTPException(503, f"Connect failed: {e}")
        return {"message": "Connected"}


    def disconnect(self):
        self.ls_repo.disconnect()
        return {"status": "disconnected"}


    # =========== Device Methods ===========
    def get_identification(self):
        return self.ls_repo.get_identification()
        


    def get_status(self, request: Request, channel: int):
        with request.app.state.lock:
            return self.ls_repo.get_status(channel)
        

    def set_modname(self, request: Request, modname: str):
        with request.app.state.lock:
            try:
                self.ls_repo.set_modname(modname)
                return {"message": "Modname updated"}
            except Exception as e:
                raise HTTPException(503, f"Update failed: {e}")
            

    def set_brightness(self, request: Request, brightness: int):
        with request.app.state.lock:
            try:
                self.ls_repo.set_brightness(brightness)
                return {"message": "Brightness updated"}
            except ValueError as e:
                raise HTTPException(400, f"Invalid brightness value: {e}")
            except Exception as e:
                raise HTTPException(503, f"Update failed: {e}")

    # =========== Reading Methods ===========
    def get_input_parameter(self, request: Request, channel: int) -> InputParameter:
        with request.app.state.lock:
            return self.ls_repo.get_input_parameter(channel)


    def set_input_config(self, request: Request, input_param: InputParameter, channel: int):
        with request.app.state.lock:
            try:
                self.ls_repo.set_input_config(input_param, channel)
                return {"message": "Input configuration updated"}
            except Exception as e:
                raise HTTPException(503, f"Update failed: {e}")


    def get_monitor(self, request: Request, channel: int) -> MonitorResp:
        with request.app.state.lock:
            return self.ls_repo.get_monitor(channel)
            
            

    # =========== Curve Methods ===========

    def get_curve_header(self, request: Request, channel: int):
        with request.app.state.lock:
            return self.ls_repo.get_curve_header(channel)


    def get_curve_data_point(self, request: Request, channel: int, index: int) -> CurveDataPoint:
        with request.app.state.lock:
            return self.ls_repo.get_curve_data_point(channel, index)    
     
    def get_curve_data_points(self, request: Request, channel: int) -> CurveDataPoints:
        with request.app.state.lock:
            return self.ls_repo.get_curve_data_points(channel)
            

    def set_curve_header(self, request: Request, curve_header: CurveHeader, channel: int):
        with request.app.state.lock:
            try:
                self.ls_repo.set_curve_header(curve_header, channel)
                return {"message": "Curve header updated"}
            except Exception as e:
                raise HTTPException(503, f"Update failed: {e}")
            

    def set_curve_data_point(self, request: Request, data_point: CurveDataPoint, channel: int, index: int):
        with request.app.state.lock:
            try:
                self.ls_repo.set_curve_data_point(data_point, channel, index)
                return {"message": "Curve data point updated"}
            except Exception as e:
                raise HTTPException(503, f"Update failed: {e}")

