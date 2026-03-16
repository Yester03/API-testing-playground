from fastapi import APIRouter, Form, Request

from app.utils.response import ok

router = APIRouter(prefix="/echo", tags=["echo"])


@router.get("/query")
def echo_query(request: Request):
    return ok(dict(request.query_params))


@router.post("/json")
async def echo_json(request: Request):
    body = await request.json()
    return ok(body)


@router.post("/form")
def echo_form(username: str = Form(...), remark: str = Form("")):
    return ok({"username": username, "remark": remark})


@router.get("/headers")
def echo_headers(request: Request):
    keys = ["user-agent", "x-request-id", "authorization", "content-type"]
    out = {k: request.headers.get(k) for k in keys}
    return ok(out)


@router.get("/cookies")
def echo_cookies(request: Request):
    return ok(request.cookies)
