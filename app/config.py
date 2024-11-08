from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "78b84c2e69f44566d3d56ea023246c0e5d425a5979edde6218713e8d3c6d0468"
    CLIENT_ID: str = "382343599423-ht51jbncsv739s1kqd8c48pv60p1rmh8.apps.googleusercontent.com"
    CLIENT_SECRET: str = "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"
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    class Config:
        env_file = ".env"

settings = Settings()

# API Documentation metadata
tags_metadata = [
    {
        "name": "authentication",
        "description": "Operations for user authentication with Google SSO"
    },
    {
        "name": "user_numbers",
        "description": "Operations with user's stored numbers"
    }
] 