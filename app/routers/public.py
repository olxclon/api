from fastapi import APIRouter

from app.db import get_categories, get_cities, get_listings
from app.schemas import Category, City, Listing

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
@router.get("/listings", response_model=list[Listing])
def list_listings() -> list[Listing]:
    return get_listings()


@router.get("/cities", response_model=list[City])
def list_cities() -> list[City]:
    return get_cities()


@router.get("/categories", response_model=list[Category])
def list_categories() -> list[Category]:
    return get_categories()
