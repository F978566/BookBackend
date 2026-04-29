from uuid import UUID
from didiator import Mediator
from fastapi import APIRouter
# from fastapi.params import Depends
from dishka.integrations.fastapi import inject, FromDishka, DishkaRoute

from src.application.book.command import (
    CreateBook,
    ChangeBookStatus,
    AddBookAuthor,
    AddBookRedactor,
)
from src.application.book.query import GetAllBooksByAuthorId
# from src.di.mediator import get_mediator

book_router = APIRouter(
    prefix="/book",
    tags=["book"],
    route_class=DishkaRoute,
)


@book_router.post("/create/")
@inject
async def create_book(
    new_book: CreateBook,
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(new_book))

@book_router.get("/get_all_books_by_author_id/{author_id}")
@inject
async def get_all_books_by_author_id(
    author_id: UUID,
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(GetAllBooksByAuthorId(author_id)))

@book_router.patch("/change_book_status")
@inject
async def change_book_status(
    change_book_status: ChangeBookStatus,
    # mediator: Mediator = Depends(get_mediator), # type: ignore
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(change_book_status))

@book_router.post("/add_book_author")
@inject
async def add_book_author(
    change_book_status: AddBookAuthor,
    # mediator: Mediator = Depends(get_mediator), # type: ignore
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(change_book_status))

@book_router.post("/add_book_redactor")
@inject
async def add_book_redactor(
    change_book_status: AddBookRedactor,
    # mediator: Mediator = Depends(get_mediator), # type: ignore
    mediator: FromDishka[Mediator], # type: ignore
):
    return (await mediator.send(change_book_status))
