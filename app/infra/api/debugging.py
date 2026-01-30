from asyncio import get_running_loop, create_task
from uuid import UUID

from fastapi import APIRouter
from starlette.websockets import WebSocket

from app.service.debugging import handle_debugging_start
from app.service.post_debugger_manager import PostDebuggerManager

router = APIRouter()


@router.websocket("/api/v1/debug/{uuid}")
async def debug(websocket: WebSocket, uuid: UUID) -> None:
    await websocket.accept()

    await handle_debugging_start(uuid)
    debugger_manager = PostDebuggerManager(uuid, get_running_loop())
    debugging_task = create_task(debugger_manager.run_debugging())

    try:
        while True:
            command = await websocket.receive_text()
            command = command.strip()
            print(f"New command: \"{command}\"")

            command_result = await debugger_manager.run_command(command)
            await websocket.send_text(command_result)
    except Exception as e:
        print(f"An exception was thrown: {e}")
