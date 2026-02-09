from asyncio import get_running_loop, create_task
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.core.command import Command
from app.service.initializing import debugging_initializer
from app.service.manager import PostDebuggerManager
from app.service.request_processing import TranslatorOutput, CodeInfo, debugging_request_processor

debugging_prefix = "/debugging"

router = APIRouter(prefix=debugging_prefix)


class DebuggingRequestPayload(BaseModel):
    post_code: str


class DebuggingRequestResult(BaseModel):
    uuid: str
    translator_output: TranslatorOutput
    code_info: CodeInfo


@router.post("/request-debugging")
async def request_debugging(payload: DebuggingRequestPayload) -> DebuggingRequestResult:
    post_code = payload.post_code
    uuid, translator_output, code_info = await debugging_request_processor.process(post_code)
    return DebuggingRequestResult(uuid=str(uuid), translator_output=translator_output, code_info=code_info)


@router.websocket("/debug/{debug_uuid}")
async def debug(websocket: WebSocket, uuid: UUID) -> None:
    await websocket.accept()

    await debugging_initializer.initialize(uuid)
    debugger_manager = PostDebuggerManager(uuid, get_running_loop())
    task = create_task(debugger_manager.run_debugging())

    while True:
        try:
            raw_command = await websocket.receive_text()
            command = await Command.from_string(raw_command)

            result = await debugger_manager.run_command(command)
            await websocket.send_text(result)
        except ValueError as e:
            print(f"An exception was thrown: {e}")
            continue
        except Exception as e:
            print(f"An exception was thrown: {e}")
            break
