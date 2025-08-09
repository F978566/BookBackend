from uuid import UUID
from didiator import Mediator
from fastapi import APIRouter
from fastapi.params import Depends

from src.application.book.command import (
    CreateBook,
    ChangeBookStatus,
    AddBookAuthor,
)
from src.application.book.query import GetAllBooksByAuthorId
from src.di.mediator import get_mediator

book_router = APIRouter(
    prefix="/book",
    tags=["book"]
)


@book_router.post("/create/")
async def create_book(
    new_book: CreateBook,
    mediator: Mediator = Depends(get_mediator), # type: ignore
):
    return (await mediator.send(new_book))

@book_router.get("/get_all_books_by_author_id/{author_id}")
async def get_all_books_by_author_id(
    author_id: UUID,
    mediator: Mediator = Depends(get_mediator), # type: ignore
):
    return (await mediator.send(GetAllBooksByAuthorId(author_id)))

@book_router.patch("/change_book_status")
async def change_book_status(
    change_book_status: ChangeBookStatus,
    mediator: Mediator = Depends(get_mediator), # type: ignore
):
    return (await mediator.send(change_book_status))

@book_router.post("/add_book_author")
async def add_book_author(
    change_book_status: AddBookAuthor,
    mediator: Mediator = Depends(get_mediator), # type: ignore
):
    return (await mediator.send(change_book_status))
