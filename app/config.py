from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# API Documentation metadata
tags_metadata = [
    {
        "name": "authentication",
        "description": "Operations for user authentication with Google SSO"
    },
    {
        "name": "user_data",
        "description": "Operations with user's stored data"
    }
] 