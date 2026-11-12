import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi import FastAPI, APIRouter, Query, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

load_dotenv()

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
def verify_api_key(api_key: str = Depends(api_key_header)):
    if not API_KEY or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

    return api_key

class Item(BaseModel):
    id: int
    name: str = Field(min_length=1)


class ItemsResponse(BaseModel):
    items: list[Item]

protected_router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)
app = FastAPI(
    title="Secure API Infrastructure",
    description="A secure REST API built with FastAPI",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Secure API Infrastructure",
        "status": "running"
    }
@protected_router.get(
    "/items",
    response_model=ItemsResponse
)
def get_items(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=2, ge=1, le=100)
):
    all_items = [
        {"id": 1, "name": "Server"},
        {"id": 2, "name": "Database"},
        {"id": 3, "name": "API"}
    ]

    start = (page - 1) * limit
    end = start + limit

    return {
        "items": all_items[start:end]
    }
@protected_router.post(
    "/items",
    response_model=Item
)
def create_item(item: Item):
    return item
app.include_router(protected_router)