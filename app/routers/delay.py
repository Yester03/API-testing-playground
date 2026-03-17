import random
import time

from fastapi import APIRouter

from app.utils.response import err, ok

router = APIRouter(tags=["delay"])
unstable_counter = {"count": 0}


@router.get("/delay/{seconds}")
def delay(seconds: int):
    if seconds < 0 or seconds > 30:
        return err("seconds must be between 0 and 30", 50010, 400)
    time.sleep(seconds)
    return ok({"delayed": seconds})


@router.get("/flaky")
def flaky():
    if random.random() < 0.5:
        return err("random fail", 50011, 503)
    return ok({"message": "random success"})


@router.get("/unstable")
def unstable():
    unstable_counter["count"] += 1
    if unstable_counter["count"] <= 3:
        return err("fail before recovery", 50012, 503, data={"attempt": unstable_counter["count"]})
    return ok({"attempt": unstable_counter["count"], "message": "recovered"})
