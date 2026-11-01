import uuid
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

MEDIA_DIR = Path("media")
AVATARS_DIR = MEDIA_DIR / "avatars"
AVATARS_DIR.mkdir(parents=True, exist_ok=True)

AVATAR_SIZE = (300, 300)
MAX_AVATAR_BYTES = 10 * 1024 * 1024  # 10 MB
AVATAR_URL_PREFIX = "/media/avatars/"


def save_avatar(file: UploadFile) -> str:
    content = file.file.read()
    if len(content) > MAX_AVATAR_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Файл слишком большой (макс. 10 MB).",
        )

    try:
        image = Image.open(BytesIO(content))
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Неподдерживаемый формат файла",
        )

    image = image.resize(AVATAR_SIZE)
    name = f"{uuid.uuid4().hex}.png"
    image.save(AVATARS_DIR / name, "PNG")

    return f"{AVATAR_URL_PREFIX}{name}"


def delete_avatar(photo_url: str | None) -> None:
    if photo_url is None:
        return
    if not photo_url.startswith(AVATAR_URL_PREFIX):
        return

    old = MEDIA_DIR / photo_url.removeprefix("/media/")
    old.unlink(missing_ok=True)
