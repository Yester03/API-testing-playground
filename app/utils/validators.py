import hashlib


def make_request_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_sort(sort_by: str, allowed: set[str], default: str) -> str:
    return sort_by if sort_by in allowed else default


def validate_order(order: str) -> str:
    return "desc" if order.lower() == "desc" else "asc"
