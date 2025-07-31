from abc import abstractmethod
from typing_extensions import Protocol


class DbModelMapper[DTO, DB_MODEL](Protocol):
    @abstractmethod
    def db_model_to_dto(self, db_model: DB_MODEL) -> DTO: ...

    @abstractmethod
    def dto_to_db_model(self, model: DTO) -> DB_MODEL: ...
