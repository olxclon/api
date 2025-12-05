import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from supabase import Client, create_client

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Initialize the Supabase client using project credentials
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)


def _table(table_name: str) -> Any:
    """Return a reference to a table within the configured schema."""

    schema = (settings.database_name or "public").strip() or "public"
    if schema not in ("public", "graphql_public"):
        logger.warning(
            "Unsupported Supabase schema '%s'; falling back to 'public'.", schema
        )
        schema = "public"

    if schema == "public":
        return supabase.table(table_name)

    return supabase.schema(schema).table(table_name)


def _listings_table() -> Any:
    """Return a reference to the listings table within the configured schema."""
    return _table("listings")


def _cities_table() -> Any:
    """Return a reference to the cities table within the configured schema."""
    return _table("cities")


def _cities_table() -> Any:
    """Return a reference to the cities table within the configured schema."""
    if settings.database_name:
        return supabase.schema(settings.database_name).table("cities")
    return supabase.table("cities")


def _handle_response(response: Any) -> List[Dict[str, Any]]:
    """Validate a Supabase response and normalize errors into HTTPExceptions."""
    error: Optional[Any] = getattr(response, "error", None)
    if error:
        message = error.get("message") if isinstance(error, dict) else str(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message or "Request to Supabase failed.",
        )

    # Some versions of supabase-py expose the status code; treat 5xx as upstream failures
    status_code: int = getattr(response, "status_code", status.HTTP_200_OK)
    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Supabase service unavailable.",
        )

    data: Optional[List[Dict[str, Any]]] = getattr(response, "data", None)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Supabase returned an unexpected response.",
        )

    return data


def create_listing(listing: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new listing in Supabase."""
    response = _listings_table().insert(listing).execute()
    data = _handle_response(response)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create listing.",
        )
    return data[0]


def get_listings() -> List[Dict[str, Any]]:
    """Retrieve all listings from Supabase."""
    response = _listings_table().select("*").execute()
    return _handle_response(response)


def get_cities() -> List[Dict[str, Any]]:
    """Retrieve all cities from Supabase ordered by name."""
    response = _cities_table().select("*").order("name").execute()
    return _handle_response(response)


def get_listing_by_id(listing_id: Any) -> Dict[str, Any]:
    """Retrieve a single listing by its identifier."""
    response = _listings_table().select("*").eq("id", listing_id).limit(1).execute()
    data = _handle_response(response)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found.",
        )
    return data[0]


def update_listing(listing_id: Any, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing listing."""
    response = _listings_table().update(updates).eq("id", listing_id).execute()
    data = _handle_response(response)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found.",
        )
    return data[0]


def delete_listing(listing_id: Any) -> Dict[str, Any]:
    """Delete a listing by its identifier."""
    response = _listings_table().delete().eq("id", listing_id).execute()
    data = _handle_response(response)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found.",
        )
    return data[0]
