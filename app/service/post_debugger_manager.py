from asyncio import AbstractEventLoop
from pathlib import Path
from tempfile import gettempdir
from uuid import UUID

from app.service.communication import CommunicationQueue
from app.service.post_debugger import PostDebugger


class PostDebuggerManager:
    def __init__(self, uuid: UUID, loop: AbstractEventLoop) -> None:
        self._uuid = uuid
        self._loop = loop

        self._command_queue = CommunicationQueue()
        self._output_queue = CommunicationQueue()

        self._debugger = PostDebugger(loop, self._command_queue, self._output_queue)

    async def run_debugging(self) -> None:
        wrapper_path = Path(gettempdir()).resolve() / "postdb" / str(self._uuid) / "python_code_wrapper.py"
        await self._loop.run_in_executor(
            None,
            lambda: self._debugger.run(f"import runpy; runpy.run_path('{wrapper_path}')")
        )

    async def run_command(self, command: str) -> str:
        await self._command_queue.send_message(command)
        result = await self._output_queue.receive_message()
        return result
