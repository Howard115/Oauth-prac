# Standard library imports
import datetime

# Third-party imports
from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.base import OpenID
from jose import jwt
from pydantic import BaseModel, Field

# Configuration
SECRET_KEY = "78b84c2e69f44566d3d56ea023246c0e5d425a5979edde6218713e8d3c6d0468"
CLIENT_ID = "382343599423-ht51jbncsv739s1kqd8c48pv60p1rmh8.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# Tags metadata for API documentation
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

# App initialization
app = FastAPI(
    title="User Numbers API",
    description="An API for storing and retrieving user numbers with Google authentication",
    openapi_tags=tags_metadata
)
sso = GoogleSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:8000/auth/callback"
)

# In-memory storage (should be replaced with a database in production)
user_numbers = {}

# Pydantic models
class NumberInput(BaseModel):
    number: int = Field(..., ge=1, le=10, description="A number between 1 and 10")

# Dependencies
async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> OpenID:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
        return OpenID(**claims["pld"])
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        ) from error

# Authentication routes with tags
@app.get("/auth/login", tags=["authentication"])
async def login():
    """Redirect the user to the Google login page."""
    async with sso:
        return await sso.get_login_redirect()

@app.get("/auth/logout", tags=["authentication"])
async def logout():
    """Forget the user's session."""
    response = RedirectResponse(url="/number")
    response.delete_cookie(key="token")
    return response

@app.get("/auth/callback", tags=["authentication"])
async def login_callback(request: Request):
    """Process login and redirect the user to the protected endpoint."""
    async with sso:
        openid = await sso.verify_and_process(request)
        if not openid:
            raise HTTPException(status_code=401, detail="Authentication failed")
    
    expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode(
        {
            "pld": openid.dict(),
            "exp": expiration,
            "sub": openid.id
        },
        key=SECRET_KEY,
        algorithm="HS256"
    )
    response = RedirectResponse(url="/numbers")
    response.set_cookie(key="token", value=token, expires=expiration)
    return response

# Business logic routes with tags
@app.get("/numbers", tags=["user_numbers"])
async def get_user_number(user: OpenID = Depends(get_logged_user)):
    """Get the stored number for the logged-in user."""
    number = user_numbers.get(user.email, None)
    return {
        "message": f"Welcome, {user.email}!",
        "stored_number": number
    }

@app.post("/numbers", tags=["user_numbers"])
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