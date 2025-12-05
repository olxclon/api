from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: str


class City(BaseModel):
    id: Optional[str] = None
    name: str
    created_at: Optional[datetime] = None


class Category(BaseModel):
    id: Optional[str] = None
    name: str
    created_at: Optional[datetime] = None


class Listing(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    price: Optional[float] = None


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
