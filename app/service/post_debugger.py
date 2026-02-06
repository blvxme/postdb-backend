from _ast import FunctionDef, ClassDef, Name, Attribute
from ast import parse
from asyncio import AbstractEventLoop, run_coroutine_threadsafe
from bdb import Bdb
from pathlib import Path
from types import FrameType
from typing import Optional, Any

from app.core.command import Command, CommandName
from app.service.communication import CommunicationQueue
from app.service.output_utils import get_output_message


class PostDebugger(Bdb):
    def __init__(
            self,
            loop: AbstractEventLoop,
            command_queue: CommunicationQueue[Command],
            output_queue: CommunicationQueue[str]
    ) -> None:
        super().__init__()

        self._loop = loop

        self._command_queue = command_queue
        self._output_queue = output_queue

        self._current_frame: Optional[FrameType] = None
        self._current_locals: dict[str, Any] = {}
        self._current_globals: dict[str, Any] = {}

    def user_line(self, frame: FrameType) -> None:
        self._current_frame = frame
        self._current_locals = dict(self._current_frame.f_locals)
        self._current_globals = dict(self._current_frame.f_globals)

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
        command = await self._command_queue.receive_message()
        await self._execute_command(command)

        output_message = await get_output_message(self._current_locals, self._current_globals)
        await self._output_queue.send_message(output_message)

    async def _execute_command(self, command: Command) -> None:
        if command.name == CommandName.SET_VARIABLE:
            ...
        elif command.name == CommandName.STEP:
            self.set_step()
        elif command.name == CommandName.CONTINUE:
            self.set_continue()
        elif command.name == CommandName.QUIT:
            self.set_quit()

    # Метод для нахождения номеров строк, на которых будут поставлены точки останова
    def _find_line_numbers(self, path: Path) -> list[int]:
        if not path.exists():
            return []

        src = path.read_text(encoding="utf-8")
        tree = parse(src)

        line_numbers = []

        for node in tree.body:
            if isinstance(node, FunctionDef) and node.name == "setVariable":
                # Добавляем в список номеров строк номер строки начала функции setVariable
                if node.body:
                    # Ставим точку останова в теле функции setVariable

                    # Если поставить точку останова на строке, на которой определена сигнатура функции setVariable,
                    # то отладчик остановится только один раз (при создании функции setVariable)
                    first_body_line = node.body[0].lineno
                    line_numbers.append(first_body_line)
                else:
                    # На случай пустой функции
                    line_numbers.append(node.lineno)
            elif isinstance(node, FunctionDef) and node.name == "set_state":
                # Добавляем в список номеров строк номер строки начала функции set_state
                if node.body:
                    # Ставим точку останова в теле функции set_state

                    # Если поставить точку останова на строке, на которой определена сигнатура функции set_state,
                    # то отладчик остановится только один раз (при создании функции set_state)

                    # "+ 1" нужен для того, чтобы избежать создания точки останова на объявлении глобальной переменной
                    # (например: global Vars)
                    first_body_line = node.body[0].lineno + 1
                    line_numbers.append(first_body_line)
                else:
                    # На случай пустой функции
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
                    # Добавляем в список номеров строк номер строки начала метода run
                    if child.body:
                        # Ставим точку останова в теле метода run

                        # Если поставить точку останова на строке, на которой определена сигнатура метода run,
                        # то отладчик остановится только один раз (при создании метода run)

                        # "+ 9" нужен для того, чтобы избежать создания точки останова на объявлении глобальной переменной
                        # (например: global inVars)
                        first_body_line = child.body[0].lineno + 9
                        line_numbers.append(first_body_line)
                    else:
                        # На случай пустого метода
                        line_numbers.append(child.lineno)

            for child in class_node.body:
                if isinstance(child, ClassDef):
                    visit_class(child, current_inside)

        for node in tree.body:
            if isinstance(node, ClassDef):
                visit_class(node, False)

        line_numbers = sorted(set(line_numbers))

        return line_numbers
