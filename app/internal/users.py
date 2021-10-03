from fastapi import APIRouter, HTTPException

from app import models, utils

router = APIRouter(prefix="/users")


@router.post("/", response_model=models.UserInternal_Pydantic)
async def create_user(user: models.UserIn_Pydantic) -> models.UserInternal_Pydantic:
    user_obj = await models.Users.create(
        api_key=utils.generate_api_key(), **user.dict(exclude_unset=True)
    )
    return await models.UserInternal_Pydantic.from_tortoise_orm(user_obj)


@router.get("/{telegram_id}/", response_model=models.UserInternal_Pydantic)
async def get_user(telegram_id: int) -> models.UserInternal_Pydantic:
    return await models.UserInternal_Pydantic.from_queryset_single(
        models.Users.get(telegram_id=telegram_id)
    )


@router.put("/{telegram_id}/", response_model=models.UserInternal_Pydantic)
async def update_user(telegram_id: int, user: models.UserIn_Pydantic) -> models.UserInternal_Pydantic:
    await models.Users.filter(telegram_id=telegram_id).update(
        **user.dict(exclude_unset=True)
    )
    user_obj = await models.Users.get(telegram_id=telegram_id)
    return await models.UserInternal_Pydantic.from_tortoise_orm(user_obj)


@router.post(
    "/{telegram_id}/revoke-api-key/", response_model=models.UserInternal_Pydantic
)
async def revoke_api_key(telegram_id: int) -> models.UserInternal_Pydantic:
    await models.Users.filter(telegram_id=telegram_id).update(
        api_key=utils.generate_api_key()
    )
    user_obj = await models.Users.get(telegram_id=telegram_id)
    return await models.UserInternal_Pydantic.from_tortoise_orm(user_obj)


@router.delete("/{telegram_id}/")
async def delete_user(telegram_id: int) -> True:
    deleted_count = await models.Users.filter(telegram_id=telegram_id).delete()

    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {telegram_id} not found")

    return True
