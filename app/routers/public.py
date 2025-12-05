from fastapi import APIRouter

from app.db import get_listings
from app.schemas import Listing

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
@router.get("/listings", response_model=list[Listing])
def list_listings() -> list[Listing]:
    return get_listings()
