from fastapi import APIRouter, Depends
from fastapi_sso.sso.base import OpenID
from sqlalchemy.orm import Session

from app.models import APIKeyInput, UserData, APIKeyResponse
from app.dependencies import get_logged_user
from app.database import get_db

router = APIRouter(
    prefix="/api-keys",
    tags=["user_data"]
)

@router.get("", response_model=APIKeyResponse)
async def get_user_api_key(
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db)
):
    """Get the stored API key for the logged-in user."""
    db_data = db.query(UserData).filter(UserData.email == user.email).first()
    stored_api_key = db_data.api_key if db_data else None
    
    return APIKeyResponse(
        message=f"Welcome, {user.email}!",
        stored_api_key=stored_api_key
    )

@router.post("", response_model=APIKeyResponse)
async def store_user_api_key(
    api_key_input: APIKeyInput,
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db)
):
    """Store an API key for the logged-in user."""
    db_data = db.query(UserData).filter(UserData.email == user.email).first()
    
    if db_data:
        db_data.api_key = api_key_input.api_key
    else:
        db_data = UserData(email=user.email, api_key=api_key_input.api_key)
        db.add(db_data)
    
    db.commit()
    db.refresh(db_data)
    
    return APIKeyResponse(
        message=f"API key stored for user {user.email}",
        stored_api_key=db_data.api_key
    ) 