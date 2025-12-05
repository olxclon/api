from fastapi import APIRouter

from app.db import get_listings
from app.schemas import Listing, LoginRequest, TokenResponse
from app.security import create_access_token

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    token = create_access_token({"sub": request.email})
    return TokenResponse(access_token=token)


@router.get("/listings", response_model=list[Listing])
def list_listings() -> list[Listing]:
    return get_listings()
