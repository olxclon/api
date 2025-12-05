from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import Listing, LoginRequest, TokenResponse
from app.security import create_access_token, get_current_user

settings = get_settings()

app = FastAPI(title="API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

public_router = APIRouter(prefix="/public", tags=["public"])


@public_router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@public_router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    token = create_access_token({"sub": request.email})
    return TokenResponse(access_token=token)


private_router = APIRouter(prefix="/private", tags=["private"], dependencies=[Depends(get_current_user)])


@private_router.get("/listings", response_model=list[Listing])
def list_listings() -> list[Listing]:
    return []


app.include_router(public_router)
app.include_router(private_router)
