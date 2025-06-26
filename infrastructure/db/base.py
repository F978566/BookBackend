from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()


engine = create_async_engine(str(os.environ.get("BASE_URL")))
