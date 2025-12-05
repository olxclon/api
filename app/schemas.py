from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class Listing(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
