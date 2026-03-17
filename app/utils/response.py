from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def ok(data=None, message: str = "success", code: int = 0, status_code: int = 200):
    payload = {"code": code, "message": message, "data": data}
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))


def err(message: str, code: int, status_code: int, data=None):
    payload = {"code": code, "message": message, "data": data}
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))
