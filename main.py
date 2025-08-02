from fastapi import FastAPI
import uvicorn
from dishka.integrations.fastapi import (
    setup_dishka,
)

from src.di.app_container import container
from src.presentation.user import user_router
from src.presentation.book import book_router

app = FastAPI()

setup_dishka(container, app)

app.include_router(user_router)
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
