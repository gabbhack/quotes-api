from pydantic.main import BaseModel
from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


class Author(BaseModel):
    id: str
    name: str


class Users(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=129)
    quotes: fields.ReverseRelation["Quotes"]

    telegram_id = fields.BigIntField(unique=True)
    api_key = fields.CharField(max_length=171)


class Quotes(models.Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="quotes")
    text = fields.CharField(max_length=280)

    created_at = fields.DatetimeField(auto_now_add=True)

    def author(self) -> Author:
        return Author(id=str(self.user.id), name=self.user.name)

    class PydanticMeta:
        computed = ["author"]
        exclude = ["user"]


class QuoteIn(BaseModel):
    text: str


Tortoise.init_models(["app.models"], "models")

# Routers
User_Pydantic = pydantic_model_creator(
    Users, name="User", exclude=["telegram_id", "api_key", "quotes"]
)
UserIn_Pydantic = pydantic_model_creator(
    Users, name="UserIn", exclude=["id", "api_key", "quotes"]
)

Quote_Pydantic = pydantic_model_creator(
    Quotes, name="Quote", exclude=["user", "user_id"]
)

# Internal
UserInternal_Pydantic = pydantic_model_creator(
    Users, name="UserInternal", exclude=["quotes"]
)
