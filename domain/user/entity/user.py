from dataclasses import dataclass, field
from uuid import UUID
from uuid import uuid4

from domain.common.entity.agregate_root import AgregateRoot
from domain.user.event.user_created import UserCreated
from domain.user.event.user_deleted import UserDeleted
from domain.user.value_object.user_role import UserRole


@dataclass
class User(AgregateRoot):
    id: UUID = field(default_factory=uuid4)
    username: str = field(default_factory=str)
    password: str = field(default_factory=str)
    email: str = field(default_factory=str)
    user_role: UserRole = field(default_factory=UserRole)
    deleted: bool = field(default=False, kw_only=True)
    
    @classmethod
    def create(
        cls,
        username: str,
        password: str,
        email: str,
        user_role: UserRole,
        user_id: UUID = uuid4(),
    ) -> "User":
        user = User(id=user_id, username=username, password=password, email=email, user_role=user_role)
        user.record_event(
            UserCreated(
                id=user_id,
                username=username,
                password=password,
                email=email,
                user_role=user_role.to_raw()
            )
        )
        
        return user


    @classmethod
    def delete(
        cls,
        user_id: UUID
    ) -> "User":
        user = User(id=user_id)
        
        user.record_event(
            UserDeleted(user_id=user.id)
        )
        
        return user