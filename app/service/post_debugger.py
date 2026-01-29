from asyncio import AbstractEventLoop, run_coroutine_threadsafe
from bdb import Bdb
from types import FrameType
from typing import Optional

from app.service.communication import CommunicationQueue


class PostDebugger(Bdb):
    def __init__(
            self,
            loop: AbstractEventLoop,
            command_queue: CommunicationQueue,
            output_queue: CommunicationQueue
    ) -> None:
        super().__init__()

        self._loop = loop

        self._command_queue = command_queue
        self._output_queue = output_queue

        self._current_frame: Optional[FrameType] = None

    def user_line(self, frame: FrameType) -> None:
        self._current_frame = frame

        future = run_coroutine_threadsafe(self.handle_stop(), self._loop)
        future.result()

    async def handle_stop(self) -> None:
        # await self._output_queue.send_message(...)

        command = await self._command_queue.receive_message()
        await self._execute_command(command)

    async def _execute_command(self, command: str) -> None:
        if command == "continue":
            self.set_continue()
        elif command == "step":
            # TODO: remove this command
            self.set_step()
        elif command == "quit":
            self.set_quit()
