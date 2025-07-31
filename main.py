from fastapi import FastAPI
import uvicorn

from src.presentation.user import user_router
from src.presentation.book import book_router

app = FastAPI()
app.include_router(user_router)
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
