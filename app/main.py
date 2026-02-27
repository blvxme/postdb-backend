from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.debugging import router
from app.settings import settings

api_prefix = "/api/v1"

app = FastAPI()
app.include_router(router, prefix=api_prefix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS
)
