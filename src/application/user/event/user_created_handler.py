from src.application.common.event import EventHandler
from src.domain.user.event.user_created import UserCreated
from src.infrastructure.mapper.message_broker_mappers import map_event_to_broker_message
from src.infrastructure.message_broker.interface import BaseMessageBroker


class UserCreatedHandler(EventHandler[UserCreated]):
    def __init__(self, broker_topic: str, message_broker: BaseMessageBroker):
        self.message_broker = message_broker
        self.broker_topic = broker_topic
    
    async def __call__(self, event: UserCreated) -> None:
        print("event", event)
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=map_event_to_broker_message(event),
        )