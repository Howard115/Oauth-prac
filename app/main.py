from fastapi import FastAPI

from app.config import tags_metadata
from app.routers import auth, numbers, api_keys

app = FastAPI(
    title="User Numbers API",
    description="An API for storing and retrieving user numbers with Google authentication",
    openapi_tags=tags_metadata
)

app.include_router(auth.router)
app.include_router(numbers.router)
app.include_router(api_keys.router)