from src.application.book.dto.book import BookDto
from src.application.book.dto.page import PageDto
from src.application.common.interfaces.db_model_mapper import DbModelMapper
from src.infrastructure.db.models.book import BookModel, PageModel


class BookDbModelMapper(DbModelMapper[BookDto, BookModel]):
    def db_model_to_dto(self, db_model: BookModel) -> BookDto:
        return BookDto(
            id=db_model.id,
            title=db_model.title,
            pages=tuple[PageDto]([
                PageDto(
                    id=page.id,
                    text=page.text,
                    number=page.number,
                )
                for page in db_model.pages
            ]),
            size=db_model.size,
            authors=[author.id for author in db_model.authors],
            redactors=[redactor.id for redactor in db_model.redactors],
            status=db_model.status,
        )

    def dto_to_db_model(self, model: BookDto) -> BookModel:
        return BookModel(
            id=model.id,
            title=model.title,
            pages=tuple[PageModel]([
                PageModel(
                    id=page.id,
                    text=page.text,
                    number=page.number,
                )
                for page in model.pages
            ]),
            size=model.size,
            authors=[author for author in model.authors],
            redactors=[redactor for redactor in model.redactors],
            status=model.status,
        )
