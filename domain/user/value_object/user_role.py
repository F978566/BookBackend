from dataclasses import dataclass
from domain.common.value_object.value_object import ValueObject
from domain.user.value_object.user_role_enum import UserRoleEnum


@dataclass(frozen=True)
class UserRole(ValueObject[UserRoleEnum]):
    value: UserRoleEnum = UserRoleEnum.READER