from fastapi import APIRouter, Depends
from fastapi_sso.sso.base import OpenID
from sqlalchemy.orm import Session

from app.models import NumberInput, UserNumber, NumberResponse
from app.dependencies import get_logged_user
from app.database import get_db, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/numbers",
    tags=["user_numbers"]
)

@router.get("", response_model=NumberResponse)
async def get_user_number(
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db)
):
    """Get the stored number for the logged-in user."""
    db_number = db.query(UserNumber).filter(UserNumber.email == user.email).first()
    stored_number = db_number.number if db_number else None
    
    return NumberResponse(
        message=f"Welcome, {user.email}!",
        stored_number=stored_number
    )

@router.post("", response_model=NumberResponse)
async def store_user_number(
    number_input: NumberInput,
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db)
):
    """Store a number (1-10) for the logged-in user."""
    db_number = db.query(UserNumber).filter(UserNumber.email == user.email).first()
    
    if db_number:
        db_number.number = number_input.number
    else:
        db_number = UserNumber(email=user.email, number=number_input.number)
        db.add(db_number)
    
    db.commit()
    db.refresh(db_number)
    
    return NumberResponse(
        message=f"Number {number_input.number} stored for user {user.email}",
        stored_number=db_number.number
    ) 