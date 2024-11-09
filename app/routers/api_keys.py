from fastapi import APIRouter, Depends
from fastapi_sso.sso.base import OpenID
from sqlalchemy.orm import Session

from app.models import APIKeyInput, UserData, APIKeyResponse
from app.dependencies import get_logged_user
from app.database import get_db
from app.utils.encryption import encrypt_api_key, decrypt_api_key

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
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    stored_api_key = decrypt_api_key(db_user.api_key) if db_user and db_user.api_key else None
    
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
    encrypted_api_key = encrypt_api_key(api_key_input.api_key)
    
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    
    if db_user:
        db_user.api_key = encrypted_api_key
    else:
        db_user = UserData(email=user.email, api_key=encrypted_api_key)
        db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
    
    return APIKeyResponse(
        message=f"API key stored for user {user.email}",
        stored_api_key=api_key_input.api_key
    ) 