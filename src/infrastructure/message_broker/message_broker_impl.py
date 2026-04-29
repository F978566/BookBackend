from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from typing import AsyncIterator
import orjson

from src.infrastructure.message_broker.interface import BaseMessageBroker


class MessageBrokerImpl(BaseMessageBroker):
    def __init__(self, producer: AIOKafkaProducer, consumer: AIOKafkaConsumer):
        self.producer = producer
        self.consumer = consumer

    async def send_message(self, topic: str, value: bytes):
        await self.producer.start() # type: ignore
        try:
            await self.producer.send(topic=topic, value=value) # type: ignore
            print(f"Message sent successfully to {topic}")
        except Exception as e:
            print(f"Failed to send message to {topic}: {e}")
            raise
        # finally:
            # await self.producer.stop() # type: ignore

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]: # type: ignore
        try:
            self.consumer.subscribe(topics=[topic])
            async for message in self.consumer:
                if message.value is not None:
                    try:
                        yield orjson.loads(message.value)
                    except orjson.JSONDecodeError as e:
                        print(f"Failed to decode message: {e}")
                        continue
        except Exception as e:
            print(f"Error in consumer: {e}")
            raise

    async def stop_consuming(self, topic: str):
        self.consumer.unsubscribe() # type: ignore

    async def close(self):
        await self.consumer.stop() # type: ignore
        await self.producer.stop() # type: ignore

    async def start(self):
        await self.producer.start() # type: ignore
        await self.consumer.start() # type: ignore