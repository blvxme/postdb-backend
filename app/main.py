from fastapi import FastAPI

from app.infra.api.debug_request import router

app = FastAPI()
app.include_router(router)
