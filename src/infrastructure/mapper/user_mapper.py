from application.common.interfaces.mapper import Mapper
from application.user.dto import UserDto
from domain.user.entity.user import User
from domain.user.value_object.user_role import UserRole


class UserMapper(Mapper[User, UserDto]):
    def domain_to_dto(self, domain_model: User) -> UserDto:
        return UserDto(
            id=domain_model.id,
            username=domain_model.username,
            password=domain_model.password,
            email=domain_model.password,
            user_role=domain_model.user_role.to_raw()
        )
    
    def dto_to_domain(self, model: UserDto) -> User:
        return User(
            id=model.id,
            username=model.username,
            password=model.password,
            email=model.email,
            user_role=UserRole(model.user_role)
        )