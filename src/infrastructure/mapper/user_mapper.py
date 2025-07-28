from src.domain.user.value_object.user_role_enum import UserRoleEnum
from src.application.common.interfaces.mapper import Mapper
from src.application.user.dto import UserDto
from src.domain.user.entity.user import User
from src.domain.user.value_object.user_role import UserRole


class UserMapper(Mapper[User, UserDto]):
    def domain_to_dto(self, domain_model: User) -> UserDto:
        return UserDto(
            id=domain_model.id,
            username=domain_model.username,
            password=domain_model.password,
            email=domain_model.email,
            user_role=tuple[UserRoleEnum]([x.to_raw() for x in domain_model.user_role])
        )

    def dto_to_domain(self, model: UserDto) -> User:
        return User(
            id=model.id,
            username=model.username,
            password=model.password,
            email=model.email,
            user_role=[UserRole(x) for x in model.user_role]
        )
