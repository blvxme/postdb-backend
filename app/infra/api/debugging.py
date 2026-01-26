from uuid import UUID

from fastapi import APIRouter
from starlette.websockets import WebSocket

from app.service.debugging import handle_debugging_start
from app.service.post_debugger import PostDebugger

router = APIRouter()


@router.websocket("/api/v1/debug/{uuid}")
async def debug(websocket: WebSocket, uuid: UUID) -> None:
    await websocket.accept()

    await handle_debugging_start(uuid)
    debugger = PostDebugger()

    while True: ...
