from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from app import utils

router = APIRouter(prefix="/images", tags=["images"])


def iterdefault():
    with open("app/assets/default.jpg", "rb") as file:
        yield from file

@router.get("/{id}.jpg")
async def get_img(id: str) -> StreamingResponse:
    if id == "default":
        return StreamingResponse(iterdefault(), media_type="image/jpeg")

    path = await utils.telegram_files.get_path(id)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Image {id} not found")
    return StreamingResponse(utils.telegram_files.stream(path))
