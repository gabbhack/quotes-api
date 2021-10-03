from typing import List

from fastapi import APIRouter

from app import models

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[models.User_Pydantic])
async def get_users(offset: int = 0, limit: int = 10) -> List[models.User_Pydantic]:
    return await models.User_Pydantic.from_queryset(
        models.Users.all().offset(offset).limit(limit)
    )


@router.get("/{id}/", response_model=models.User_Pydantic)
async def get_user(id: str) -> models.User_Pydantic:
    return await models.User_Pydantic.from_queryset_single(models.Users.get(id=id))


@router.get("/{id}/quotes/", response_model=List[models.Quote_Pydantic])
async def get_user_quotes(id: str, offset: int = 0, limit: int = 10) -> List[models.Quote_Pydantic]:
    quotes = (
        await models.Quotes.filter(user__id=id)
        .offset(offset)
        .limit(limit)
        .order_by("-created_at")
        .prefetch_related("user")
    )
    return [
        models.Quote_Pydantic(
            id=quote_obj.id,
            text=quote_obj.text,
            created_at=quote_obj.created_at,
            author=models.Author(id=str(quote_obj.user.id), name=quote_obj.user.name, avatar=quote_obj.user.avatar),
        )
        for quote_obj in quotes
    ]
