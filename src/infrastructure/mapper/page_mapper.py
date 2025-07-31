from src.application.book.dto.page import PageDto
from src.application.common.interfaces.mapper import DomainMapper
from src.domain.book.entity.page import Page


class PageMapper(DomainMapper[Page, PageDto]):
    def domain_to_dto(self, domain_model: Page) -> PageDto:
        return PageDto(
            id=domain_model.id,
            text=domain_model.text,
            number=domain_model.number,
        )

    def dto_to_domain(self, model: PageDto) -> Page:
        return Page(
            id=model.id,
            text=model.text,
            number=model.number,
        )
