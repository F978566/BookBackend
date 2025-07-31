from didiator import Mediator
from fastapi import APIRouter
from fastapi.params import Depends

from src.application.book.command.create_book import CreateBook
from src.di.mediator import get_mediator

book_router = APIRouter(
    prefix="/book",
    tags=["book"]
)


@book_router.post("/create/")
async def create_book(
    mediator: Mediator = Depends(get_mediator), # type: ignore
    new_book: CreateBook | None = None,
):
    return (await mediator.send(new_book))
