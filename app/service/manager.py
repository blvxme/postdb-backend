from asyncio import AbstractEventLoop
from uuid import UUID

from app.config import config
from app.core.command import Command
from app.core.communication import CommunicationQueue
from app.core.debugger import PostDebugger


class PostDebuggerManager:
    def __init__(self, uuid: UUID, loop: AbstractEventLoop) -> None:
        self._uuid = uuid
        self._loop = loop

        self._command_queue = CommunicationQueue[Command]()
        self._output_queue = CommunicationQueue[str]()

        self._debugger = PostDebugger(loop, self._command_queue, self._output_queue)

    async def run_debugging(self) -> None:
        python_code_path = config.TRANSLATION_PATH / str(self._uuid) / "python_code.py"

        python_code_source = None
        with open(python_code_path, "r", encoding="utf-8") as f:
            python_code_source = f.read()

        python_code = compile(python_code_source, python_code_path, "exec")

        def run_debugger() -> None:
            try:
                self._debugger.set_breakpoints(python_code_path)
            except Exception as e:
                print(f"Failed to set breakpoints: {e}")

            self._debugger.run(python_code)

        await self._loop.run_in_executor(None, run_debugger)

    async def run_command(self, command: Command) -> str:
        await self._command_queue.send_message(command)
        result = await self._output_queue.receive_message()
        return result
