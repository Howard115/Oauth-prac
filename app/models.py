from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field

from .database import Base

# Pydantic model for input validation
class NumberInput(BaseModel):
    number: int = Field(..., ge=1, le=10, description="A number between 1 and 10")

# SQLAlchemy model for database
class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    number = Column(Integer)
    api_key = Column(String)

# Pydantic model for response
class NumberResponse(BaseModel):
    message: str
    stored_number: int | None

    class Config:
        from_attributes = True

# Add after the NumberResponse class

class APIKeyInput(BaseModel):
    api_key: str = Field(..., min_length=1, max_length=256, description="User's personal API key")

class APIKeyResponse(BaseModel):
    message: str
    stored_api_key: str | None

    class Config:
        from_attributes = True