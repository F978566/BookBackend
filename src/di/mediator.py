from dishka import AsyncContainer

from didiator import Mediator
from didiator.ioc.dishka import DishkaIoc
from didiator.mediator import MediatorImpl
from src.application.book.command import (
    AddBookPage,
    AddBookPageHandler,
    CreateBook,
    CreateBookHandler,
)
from src.application.book.query import GetAllBooksByAuthorId, GetAllBooksByAuthorIdHandler
from src.application.user.command.create_user import CreateUser, CreateUserHandler
from .app_container import container


def build_mediator(container: AsyncContainer) -> Mediator:
    mediator = MediatorImpl(ioc=DishkaIoc(container), middlewares=[])

    mediator.register_request_handler(CreateUser, CreateUserHandler)
    mediator.register_request_handler(CreateBook, CreateBookHandler)
    mediator.register_request_handler(AddBookPage, AddBookPageHandler)
    mediator.register_request_handler(GetAllBooksByAuthorId, GetAllBooksByAuthorIdHandler)

    return mediator


def get_mediator() -> Mediator:
    mediator = build_mediator(container)

    return mediator
