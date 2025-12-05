from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.schemas import TokenData

settings = get_settings()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    return create_access_token(
        {**data, "type": "refresh"}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def verify_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception
        if payload.get("type") == "refresh":
            raise credentials_exception
        return TokenData(sub=subject, type=payload.get("type"))
    except JWTError as exc:  # pragma: no cover - defensive logging
        raise credentials_exception from exc


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    return verify_token(token)


def verify_refresh_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "invalid_token", "message": "Invalid refresh token."},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception
        return TokenData(sub=subject, type=payload.get("type"))
    except JWTError as exc:  # pragma: no cover - defensive logging
        raise credentials_exception from exc
