from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.config import settings
from app.utils.response import err, ok

router = APIRouter(prefix="/upload", tags=["upload"])
ALLOWED_EXT = {".txt", ".csv", ".json", ".png", ".jpg", ".jpeg", ".pdf"}


def _save_file(file: UploadFile):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXT:
        return None, "invalid file type"

    content = file.file.read()
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_size:
        return None, f"file too large, max {settings.MAX_UPLOAD_SIZE_MB}MB"

    out_path = Path(settings.UPLOAD_DIR) / file.filename
    out_path.write_bytes(content)
    return {"filename": file.filename, "size": len(content)}, None


@router.post("/single")
def upload_single(file: UploadFile = File(...)):
    saved, error = _save_file(file)
    if error:
        return err(error, 40020, 400)
    return ok(saved, message="uploaded")


@router.post("/multiple")
def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for f in files:
        saved, error = _save_file(f)
        if error:
            return err(f"{f.filename}: {error}", 40020, 400)
        results.append(saved)
    return ok(results, message="uploaded")


@router.get("/files")
def list_files():
    p = Path(settings.UPLOAD_DIR)
    files = [{"filename": f.name, "size": f.stat().st_size} for f in p.glob("*") if f.is_file()]
    return ok(files)
