import datetime
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from jose import jwt

from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

sso = GoogleSSO(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI
)

@router.get("/login")
async def login():
    """Redirect the user to the Google login page."""
    async with sso:
        return await sso.get_login_redirect()

@router.get("/logout")
async def logout():
    """Forget the user's session."""
    response = RedirectResponse(url="/number")
    response.delete_cookie(key="token")
    return response

@router.get("/callback")
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
        key=settings.SECRET_KEY,
        algorithm="HS256"
    )
    response = RedirectResponse(url="/numbers")
    response.set_cookie(key="token", value=token, expires=expiration)
    return response 