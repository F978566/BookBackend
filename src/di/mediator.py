from dishka import AsyncContainer, make_async_container

from didiator import Mediator
from didiator.ioc.dishka import DishkaIoc
from didiator.mediator import MediatorImpl
from src.application.book.command import (
    AddBookPage,
    AddBookPageHandler,
    CreateBook,
    CreateBookHandler,
)
from src.application.user.command.create_user import CreateUser, CreateUserHandler
from src.di.app_container import AppContainer


def build_mediator(container: AsyncContainer) -> Mediator:
    mediator = MediatorImpl(ioc=DishkaIoc(container), middlewares=[])

    mediator.register_request_handler(CreateUser, CreateUserHandler)
    mediator.register_request_handler(CreateBook, CreateBookHandler)
    mediator.register_request_handler(AddBookPage, AddBookPageHandler)

    return mediator


def get_mediator() -> Mediator:
    container = make_async_container(AppContainer())
    mediator = build_mediator(container)

    return mediator
