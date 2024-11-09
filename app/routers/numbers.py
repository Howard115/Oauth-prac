from fastapi import APIRouter, Depends
from fastapi_sso.sso.base import OpenID
from sqlalchemy.orm import Session

from app.models import NumberInput, UserData, NumberResponse
from app.dependencies import get_logged_user
from app.database import get_db, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/numbers",
    tags=["user_data"]
)

@router.get("", response_model=NumberResponse)
async def get_user_number(
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db)
):
    """Get the stored number for the logged-in user."""
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    stored_number = db_user.number if db_user else None
    
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
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    
    if db_user:
        db_user.number = number_input.number
    else:
        db_user = UserData(email=user.email, number=number_input.number)
        db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
    
    return NumberResponse(
        message=f"Number {number_input.number} stored for user {user.email}",
        stored_number=db_user.number
    ) 