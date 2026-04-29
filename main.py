import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from dishka.integrations.fastapi import (
    setup_dishka,
)

from src.di.app_container import container
from src.infrastructure.message_broker.interface import BaseMessageBroker
from src.presentation.user import user_router
from src.presentation.book import book_router

async def consume_messages(message_broker: BaseMessageBroker, topic: str):
    try:
        async for message in message_broker.start_consuming(topic): # type: ignore
            print(f"Received message: {message}")
            # Add logic to dispatch messages to handlers, e.g., UserCreatedHandler
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        await message_broker.stop_consuming(topic)

@asynccontextmanager
async def lifespan(app: FastAPI):
    message_broker = await container.get(BaseMessageBroker)
    try:
        # Access the Dishka container
        print("Starting message broker...")
        await message_broker.start()

        # Start the consumer in the background
        topic = "my_topic"
        consumer_task = asyncio.create_task(consume_messages(message_broker, topic))
        print(f"Started consumer task for topic: {topic}")

        yield  # Application runs here
    except Exception as e:
        print(f"Error in lifespan startup: {e}")
        raise
    finally:
        print("Shutting down consumer task...")
        consumer_task.cancel() # type: ignore
        try:
            await consumer_task # type: ignore
        except asyncio.CancelledError:
            print("Consumer task cancelled")
        print("Closing message broker...")
        await message_broker.close()
        print("Message broker closed")

app = FastAPI(lifespan=lifespan)

setup_dishka(container, app)

app.include_router(user_router)
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
