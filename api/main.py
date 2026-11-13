import hmac
import os
import logging
import time

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi import FastAPI, APIRouter, Query, Depends, HTTPException, status, Request, Response
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

load_dotenv()
FORCE_HTTPS = os.getenv("FORCE_HTTPS", "false").lower() == "true"
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1"
]
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    headers_enabled=True
)

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
def verify_api_key(api_key: str = Depends(api_key_header)):
    if not API_KEY or not api_key or not hmac.compare_digest(api_key, API_KEY):
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
class RequestSizeLimitMiddleware:
    def __init__(self, app, max_body_size=1048576):
        self.app = app
        self.max_body_size = max_body_size

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        body = bytearray()

        while True:
            message = await receive()

            if message["type"] == "http.disconnect":
                return

            if message["type"] == "http.request":
                body.extend(message.get("body", b""))

                if len(body) > self.max_body_size:
                    response = JSONResponse(
                        status_code=413,
                        content={"detail": "Request body too large"}
                    )
                    await response(scope, receive, send)
                    return

                if not message.get("more_body", False):
                    break

        body_bytes = bytes(body)
        sent = False

        async def replay_body():
            nonlocal sent

            if not sent:
                sent = True
                return {
                    "type": "http.request",
                    "body": body_bytes,
                    "more_body": False
                }

            return {
                "type": "http.request",
                "body": b"",
                "more_body": False
            }

        await self.app(scope, replay_body, send)

       
app = FastAPI(
    title="Secure API Infrastructure",
    description="A secure REST API built with FastAPI",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)
app.add_middleware(
    RequestSizeLimitMiddleware,
    max_body_size=1048576
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Content-Type"]
)
if FORCE_HTTPS:
    app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS
)

async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unexpected error on %s",
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    duration = (time.perf_counter() - start_time) * 1000

    log_level = logging.WARNING if duration > 1000 else logging.INFO

    logger.log(
        log_level,
        "%s %s - Status: %s - Duration: %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        duration
    )

    return response


app.add_exception_handler(
    Exception,
    global_exception_handler
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
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
@limiter.limit("5/minute")

def get_items(
    request: Request,
    response: Response,
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
@limiter.limit("5/minute")
def create_item(
    request: Request,
    response: Response,
    item: Item
):
    return item
app.include_router(protected_router)