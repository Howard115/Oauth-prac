from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field

from .database import Base

# Pydantic model for input validation
class NumberInput(BaseModel):
    number: int = Field(..., ge=1, le=10, description="A number between 1 and 10")

# SQLAlchemy model for database
class UserNumber(Base):
    __tablename__ = "user_numbers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    number = Column(Integer)

# Pydantic model for response
class NumberResponse(BaseModel):
    message: str
    stored_number: int | None

    class Config:
        from_attributes = True 