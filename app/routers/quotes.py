from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app import models, dependencies

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/", response_model=List[models.Quote_Pydantic])
async def get_quotes(offset: int = 0, limit: int = 10) -> List[models.Quote_Pydantic]:
    quotes = (
        await models.Quotes.all()
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


@router.get("/{id}/", response_model=models.Quote_Pydantic)
async def get_quote(id: str) -> models.Quote_Pydantic:
    quote_obj = await models.Quotes.get(id=id).prefetch_related("user")
    return models.Quote_Pydantic(
        id=quote_obj.id,
        text=quote_obj.text,
        created_at=quote_obj.created_at,
        author=models.Author(id=str(quote_obj.user.id), name=quote_obj.user.name, avatar=quote_obj.user.avatar),
    )


@router.post("/", response_model=models.Quote_Pydantic)
async def create_quote(
    quote: models.QuoteIn,
    user: models.Users = Depends(dependencies.get_current_user),
) -> models.Quote_Pydantic:
    quote_obj = await models.Quotes.create(user=user, **quote.dict(exclude_unset=True))
    return models.Quote_Pydantic(
        id=quote_obj.id,
        text=quote_obj.text,
        created_at=quote_obj.created_at,
        author=models.Author(id=str(quote_obj.user.id), name=quote_obj.user.name, avatar=quote_obj.user.avatar),
    )


@router.put("/{id}/", response_model=models.Quote_Pydantic)
async def update_quote(
    id: str,
    quote: models.QuoteIn,
    user: models.Users = Depends(dependencies.get_current_user),
) -> models.Quote_Pydantic:
    await user.quotes.filter(id=id).update(text=quote.text)

    quote_obj = await models.Quotes.get(id=id).prefetch_related("user")
    return models.Quote_Pydantic(
        id=quote_obj.id,
        text=quote_obj.text,
        created_at=quote_obj.created_at,
        author=models.Author(id=str(quote_obj.user.id), name=quote_obj.user.name, avatar=quote_obj.user.avatar),
    )


@router.delete("/{id}/", response_model=bool)
async def delete_quote(
    id: str, user: models.Users = Depends(dependencies.get_current_user)
) -> True:
    deleted_count = await user.quotes.filter(id=id).delete()

    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Quote {id} not found")
    return True
