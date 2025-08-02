from didiator import Mediator
from fastapi import APIRouter
from fastapi.params import Depends

from src.application.user.command.create_user import CreateUser
from src.di.mediator import get_mediator

user_router = APIRouter(
    tags=["user"]
)


@user_router.post("/create/")
async def create_user(
    new_user: CreateUser,
    mediator: Mediator = Depends(get_mediator), # type: ignore
):
    return (await mediator.send(new_user))
