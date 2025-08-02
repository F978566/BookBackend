from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.application.book.dto.book import BookDto
from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.query import Query, QueryHandler


@dataclass
class GetAllBooksByAuthorId(Query[List[BookDto]]):
    author_id: UUID
    

class GetAllBooksByAuthorIdHandler(QueryHandler[GetAllBooksByAuthorId, List[BookDto]]):
    def __init__(
        self,
        book_repo: BookRepo,
    ):
        self.book_repo = book_repo
    
    async def __call__(self, request: GetAllBooksByAuthorId) -> List[BookDto]:
        return (await self.book_repo.get_all_books_by_author(request.author_id))