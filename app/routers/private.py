from fastapi import APIRouter, Depends

from app.db import create_listing, delete_listing, update_listing
from app.schemas import Listing, ListingUpdate
from app.security import get_current_user

router = APIRouter(
    prefix="/private", tags=["private"], dependencies=[Depends(get_current_user)]
)


@router.post("/listings", response_model=Listing)
def create_listing_handler(listing: Listing) -> Listing:
    created = create_listing(listing.dict(exclude_none=True))
    return Listing(**created)


@router.patch("/listings/{listing_id}", response_model=Listing)
def update_listing_handler(listing_id: str, listing: ListingUpdate) -> Listing:
    updated = update_listing(listing_id, listing.dict(exclude_none=True))
    return Listing(**updated)


@router.delete("/listings/{listing_id}", response_model=Listing)
def delete_listing_handler(listing_id: str) -> Listing:
    deleted = delete_listing(listing_id)
    return Listing(**deleted)
