import fastapi
from pathlib import Path

UPLOAD_DIR = Path() / "uploads"


router = fastapi.APIRouter()


@router.post("/uploadfile")
async def upload_file(file: fastapi.UploadFile):
    data = await file.read()
    save_to = UPLOAD_DIR / file.filename
    with open(save_to, "wb") as f:
        f.write(data)
    return {"filename": file.filename}
