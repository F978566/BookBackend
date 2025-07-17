from enum import Enum


class BookStatusEnum(Enum):
    IN_PROGRESS = "in_progress"
    PUBLISHED = "published"
    APROOVED = "aprooved"
    DENIED = "denied"
