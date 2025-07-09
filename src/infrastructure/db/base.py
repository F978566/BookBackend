from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os

load_dotenv()


engine = create_async_engine(str(os.environ.get("BASE_URL")))


async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
