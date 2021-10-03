from fastapi import FastAPI
from fastapi.param_functions import Depends
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from app.routers import quotes, users, index
from app.internal import users as admin_users
from app import dependencies, config

app = FastAPI(
    title="Quotes",
    version="0.1.0",
    contact={
        "name": "Telegram bot",
        "url": "http://t.me/apiquotesbot"
    },
    responses={
        404: {
            "model": HTTPNotFoundError
        }
    }
)

app.include_router(index.router)
app.include_router(quotes.router)
app.include_router(users.router)
app.include_router(
    admin_users.router,
    prefix="/internal",
    dependencies=[Depends(dependencies.is_bot)],
    include_in_schema=False,
)
register_tortoise(
    app,
    config=config.TORTOISE_ORM,
    add_exception_handlers=True,
)
