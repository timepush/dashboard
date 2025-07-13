from fastapi import APIRouter, HTTPException, Response, Request, status
from api.features.auth.models import UserInManual, UserInOAuth, LoginRequest, TokenOut, RefreshRequest
from api.features.auth.service import signup_manual, login_manual, login_or_register_oauth, refresh_access_token, InvalidCredentialsError, NotVerifiedError
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=dict)
async def signup(user: UserInManual):
    try:
        await signup_manual(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"msg": "User created"}


@router.post("/signin", response_model=TokenOut)
async def signin(data: LoginRequest, response: Response):
    try:
        token, refresh_token = await login_manual(data.email, data.password)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=not os.getenv("DEV", False),
            samesite="lax",
            max_age=60*60*24*7,  # 7 days
            path="/"
        )
        return {"token": token}
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="The email or password you entered is incorrect. Please try again.")
    except NotVerifiedError:
        raise HTTPException(status_code=403, detail="Your email address has not been verified. Please check your inbox for a verification link.")


@router.post("/refresh", response_model=TokenOut)
async def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        token = await refresh_access_token(refresh_token)
        return {"token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
async def signout(response: Response):
    response.delete_cookie(key="refresh_token", path="/")
    return
