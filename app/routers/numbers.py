from fastapi import APIRouter, Depends
from fastapi_sso.sso.base import OpenID

from app.models import NumberInput
from app.dependencies import get_logged_user

router = APIRouter(
    prefix="/numbers",
    tags=["user_numbers"]
)

# In-memory storage (should be replaced with a database in production)
user_numbers = {}

@router.get("")
async def get_user_number(user: OpenID = Depends(get_logged_user)):
    """Get the stored number for the logged-in user."""
    number = user_numbers.get(user.email, None)
    return {
        "message": f"Welcome, {user.email}!",
        "stored_number": number
    }

@router.post("")
async def store_user_number(
    number_input: NumberInput,
    user: OpenID = Depends(get_logged_user)
):
    """Store a number (1-10) for the logged-in user."""
    user_numbers[user.email] = number_input.number
    return {
        "message": f"Number {number_input.number} stored for user {user.email}",
        "stored_number": number_input.number
    } 