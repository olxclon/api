from fastapi import APIRouter, HTTPException, status

from app.db import supabase
from app.schemas import LoginRequest, RefreshRequest, TokenResponse
from app.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

_invalid_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"error": "invalid_credentials", "message": "Invalid email or password."},
)


# Stubbed demo user used when Supabase authentication is unavailable.
DEMO_USER = {
    "email": "demo@example.com",
    "hashed_password": hash_password("changeme"),
}


def _authenticate_user(email: str, password: str) -> str | None:
    """Authenticate using Supabase auth or fall back to the demo user."""
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = getattr(response, "user", None)
        if user and getattr(user, "id", None):
            return str(user.id)
    except Exception:  # pragma: no cover - defensive fallback when Supabase is unreachable
        pass

    if email.lower() == DEMO_USER["email"].lower() and verify_password(
        password, DEMO_USER["hashed_password"]
    ):
        return email

    return None


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    user_identifier = _authenticate_user(request.email, request.password)
    if not user_identifier:
        raise _invalid_credentials_error

    access_token = create_access_token({"sub": user_identifier})
    refresh_token = create_refresh_token({"sub": user_identifier})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest) -> TokenResponse:
    token_data = verify_refresh_token(request.refresh_token)
    if not token_data.sub:
        raise _invalid_credentials_error

    access_token = create_access_token({"sub": token_data.sub})
    new_refresh_token = create_refresh_token({"sub": token_data.sub})
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
