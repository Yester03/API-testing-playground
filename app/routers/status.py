from fastapi import APIRouter

from app.utils.response import err, ok

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/200")
def s200():
    return ok({"status": 200})


@router.get("/201")
def s201():
    return ok({"status": 201}, status_code=201)


@router.get("/400")
def s400():
    return err("bad request demo", 1400, 400)


@router.get("/401")
def s401():
    return err("unauthorized demo", 1401, 401)


@router.get("/403")
def s403():
    return err("forbidden demo", 1403, 403)


@router.get("/404")
def s404():
    return err("not found demo", 1404, 404)


@router.get("/409")
def s409():
    return err("conflict demo", 1409, 409)


@router.get("/422")
def s422():
    return err("validation demo", 1422, 422)


@router.get("/500")
def s500():
    return err("internal error demo", 1500, 500)
