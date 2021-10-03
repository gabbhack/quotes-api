from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.models import Users
from app.config import BOT_API_KEY

api_key_scheme = APIKeyHeader(name="x-api-key")


async def get_current_user(api_key: str = Depends(api_key_scheme)) -> Users:
    user = await Users.get_or_none(api_key=api_key)
    if user is None:
        raise HTTPException(status_code=400, detail="x-api-key header invalid")
    return user


async def is_bot(api_key: str = Depends(api_key_scheme)) -> True:
    if api_key != BOT_API_KEY:
        raise HTTPException(status_code=400, detail="x-api-key header invalid")
    return True
