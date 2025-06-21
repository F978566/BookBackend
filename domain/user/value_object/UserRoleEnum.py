from enum import Enum


class UserRoleEnum(Enum):
    MODERATOR = "moderator"
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"
