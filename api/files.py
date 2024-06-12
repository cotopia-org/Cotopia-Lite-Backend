import fastapi
from api.utils.file import validate_file, UPLOAD_DIR

router = fastapi.APIRouter()


@router.post("/uploadfile")
async def upload_file(file: fastapi.UploadFile):
    validate_file(file=file)
    data = await file.read()
    save_to = UPLOAD_DIR / file.filename
    with open(save_to, "wb") as f:
        f.write(data)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }
