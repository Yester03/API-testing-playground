from fastapi.responses import JSONResponse


def ok(data=None, message: str = "success", code: int = 0, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={"code": code, "message": message, "data": data},
    )


def err(message: str, code: int, status_code: int, data=None):
    return JSONResponse(
        status_code=status_code,
        content={"code": code, "message": message, "data": data},
    )
