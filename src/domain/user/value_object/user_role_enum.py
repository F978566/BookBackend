from enum import Enum


class UserRoleEnum(Enum):
    MODERATOR = "moderator"
    ADMIN = "admin"
    WRITER = "writer"
    READER = "reader"
