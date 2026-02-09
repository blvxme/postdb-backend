from fastapi import FastAPI

from app.api.v1.debugging import router

api_prefix = "/api/v1"

app = FastAPI()
app.include_router(router, prefix=api_prefix)
