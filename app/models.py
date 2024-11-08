from pydantic import BaseModel, Field

class NumberInput(BaseModel):
    number: int = Field(..., ge=1, le=10, description="A number between 1 and 10") 