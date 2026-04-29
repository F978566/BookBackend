from didiator import Mediator
from fastapi import APIRouter
# from fastapi.params import Depends
from dishka.integrations.fastapi import inject, FromDishka, DishkaRoute

from src.application.user.command.add_user_role import AddUserRole
from src.application.user.command.create_user import CreateUser
# from src.di.mediator import get_mediator

user_router = APIRouter(
    tags=["user"],
    route_class=DishkaRoute,
)


@user_router.post("/create/")
@inject
async def create_user(
    new_user: CreateUser,
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(new_user))


@user_router.post("/add_user_role/")
@inject
async def add_user_role(
    new_role: AddUserRole,
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(new_role))
