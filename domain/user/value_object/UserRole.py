from domain.common.value_object.value_object import ValueObject
from domain.user.value_object.UserRoleEnum import UserRoleEnum


class UserRole(ValueObject[UserRoleEnum]):
    value: UserRoleEnum = UserRoleEnum.READER