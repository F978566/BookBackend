from uuid import UUID
from didiator import Mediator
from fastapi import APIRouter
from fastapi.params import Depends

from src.application.book.command.create_book import CreateBook
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
