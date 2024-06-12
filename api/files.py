import fastapi
from pathlib import Path

from fastapi import HTTPException, status
from typing import IO
import filetype

UPLOAD_DIR = Path() / "uploads"
MAX_FILE_SIZE = 4 * 2097152  # 8MB
ALLOWED_FILE_TYPES = [
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/heic",
    "image/heif",
    "image/heics",
    "png",
    "jpeg",
    "jpg",
    "heic",
    "heif",
    "heics",
]


def validate_file(file: IO):

    file_info = filetype.guess(file.file)
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type",
        )

    detected_content_type = file_info.extension.lower()

    if (
        file.content_type not in ALLOWED_FILE_TYPES
        or detected_content_type not in ALLOWED_FILE_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large"
            )


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
