
from fastapi import Depends, HTTPException, status, Request
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from api.common.config import settings
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

# Password helpers


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

# JWT helpers


def create_jwt_token(user_id: str, expires_delta: int = None) -> str:
    user_id_str = str(user_id)
    expire = datetime.utcnow() + timedelta(seconds=expires_delta or 900)
    to_encode = {"sub": user_id_str, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    user_id_str = str(user_id)
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": user_id_str, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])


# FastAPI dependency to get current user_id from Authorization header
async def get_current_user_id(request: Request) -> UUID:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_jwt_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return UUID(user_id)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
