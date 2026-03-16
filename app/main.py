from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import admin, auth, delay, echo, idempotent, items, orders, status, upload, users
from app.utils.response import err, ok
from app.utils.homepage import render_homepage
from app.utils.seed import seed_data

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)


def init_app():
    Path(settings.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_app()


@app.exception_handler(PermissionError)
async def permission_error_handler(_: Request, exc: PermissionError):
    message = str(exc)
    status_code = 401 if "token" in message or "missing bearer" in message else 403
    return err(message, 10012 if status_code == 401 else 10013, status_code)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"code": 1422, "message": "validation error", "data": exc.errors()},
    )


@app.get("/", include_in_schema=False)
def root():
    return render_homepage(settings.APP_NAME, settings.APP_VERSION)


@app.get("/health")
def health():
    return ok({"status": "ok", "env": settings.APP_ENV})


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(orders.router)
app.include_router(upload.router)
app.include_router(echo.router)
app.include_router(status.router)
app.include_router(delay.router)
app.include_router(idempotent.router)
app.include_router(admin.router)
