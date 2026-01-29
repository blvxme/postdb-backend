from _ast import FunctionDef, ClassDef, Name, Attribute
from ast import parse
from asyncio import AbstractEventLoop, run_coroutine_threadsafe
from bdb import Bdb
from pathlib import Path
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

    def set_breakpoints(self, path: Path) -> None:
        line_numbers = self._find_line_numbers(path)
        if not line_numbers:
            print(f"Line numbers not found: {path}")
            return

        filename = str(path)
        print(f"File name: {filename}")

        for line_number in line_numbers:
            try:
                self.set_break(filename, line_number)
                print(f"Breakpoint set at {filename}:{line_number}")
            except Exception as e:
                print(f"Failed to set breakpoint at {filename}:{line_number}: {e}")

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

    def _find_line_numbers(self, path: Path) -> list[int]:
        if not path.exists():
            return []

        src = path.read_text(encoding="utf-8")
        tree = parse(src)

        line_numbers = []

        for node in tree.body:
            if isinstance(node, FunctionDef) and node.name in ("set_state", "setVariable"):
                line_numbers.append(node.lineno)

        def visit_class(class_node: ClassDef, inside_program: bool) -> None:
            inherits_program = any(
                (isinstance(base, Name) and base.id == "Program") or
                (isinstance(base, Attribute) and getattr(base, "attr", None) == "Program")
                for base in class_node.bases
            )

            current_inside = inside_program or (class_node.name == "Program") or inherits_program

            for child in class_node.body:
                if isinstance(child, FunctionDef) and child.name == "run" and current_inside:
                    line_numbers.append(child.lineno)

            for child in class_node.body:
                if isinstance(child, ClassDef):
                    visit_class(child, current_inside)

        for node in tree.body:
            if isinstance(node, ClassDef):
                visit_class(node, False)

        line_numbers = sorted(set(line_numbers))

        return line_numbers
