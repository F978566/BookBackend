from dishka import AsyncContainer

from didiator import Mediator
from didiator.ioc.dishka import DishkaIoc
from didiator.mediator import MediatorImpl
from src.application.user.command.create_user import CreateUser, CreateUserHandler


def build_mediator(container: AsyncContainer) -> Mediator:
    mediator = MediatorImpl(ioc=DishkaIoc(container), middlewares=[])

    mediator.register_request_handler(CreateUser, CreateUserHandler)
    # mediator.register_request_handler(GetUserById, handle_get_user_by_id)

    return mediator
