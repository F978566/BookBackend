from src.application.common.interfaces.db_model_mapper import DbModelMapper
from src.application.user.dto.user import UserDto
from src.infrastructure.db.models.user import UserModel
from src.domain.user.value_object.user_role_enum import UserRoleEnum


class UserDbModelMapper(DbModelMapper[UserDto, UserModel]):
    def db_model_to_dto(self, db_model: UserModel) -> UserDto:
        return UserDto(
            id=db_model.id,
            username=db_model.username,
            password=db_model.password,
            email=db_model.email,
            user_role=tuple[UserRoleEnum]([role for role in db_model.user_role]),
            deleted=db_model.deleted,
        )

    def dto_to_db_model(self, model: UserDto) -> UserModel:
        return UserModel(
            id=model.id,
            username=model.username,
            password=model.password,
            email=model.email,
            user_role=tuple[UserRoleEnum]([role for role in model.user_role]),
            deleted=model.deleted,
        )
