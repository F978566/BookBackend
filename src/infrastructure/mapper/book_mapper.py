from src.domain.book.value_objects.book_status import BookStatus
from src.application.book.dto.book import BookDto
from src.application.book.dto.page import PageDto
from src.domain.book.entity.book import Book
from src.application.common.interfaces.mapper import Mapper
from src.domain.book.entity import Page


class BookMapper(Mapper[Book, BookDto]):
    def domain_to_dto(self, domain_model: Book) -> BookDto:
        return BookDto(
            id = domain_model.id,
            title = domain_model.title,
            pages = [
                PageDto(
                    id = x.id,
                    text = x.text,
                    number = x.number
                ) for x in domain_model.pages
            ],
            size = domain_model.size,
            authors = domain_model.authors,
            redactors = domain_model.redactors,
            status = domain_model.status.value
        )

    def dto_to_domain(self, model: BookDto) -> Book:
        return Book(
            id = model.id,
            title = model.title,
            pages = [
                Page(
                    id = x.id,
                    text = x.text,
                    number = x.number
                ) for x in model.pages
            ],
            size = model.size,
            authors = model.authors,
            redactors = model.redactors,
            status = BookStatus(model.status),
        )
