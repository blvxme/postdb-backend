from fastapi import FastAPI

from app.infra.api.debug_request import router as debug_request_router
from app.infra.api.debugging import router as debugging_router

app = FastAPI()
app.include_router(debug_request_router)
app.include_router(debugging_router)
