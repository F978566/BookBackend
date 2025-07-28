from didiator import Mediator
from fastapi import APIRouter
from fastapi.params import Depends

from src.application.user.command.create_user import CreateUser
from src.domain.user.value_object.user_role_enum import UserRoleEnum
from src.di.mediator import get_mediator

user_router = APIRouter(
    tags=["user"]
)


@user_router.post("/create/")
async def create_user(
    mediator: Mediator = Depends(get_mediator),
    new_user: CreateUser | None = None,
):
    return (await mediator.send(new_user))
