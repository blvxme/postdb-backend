from dataclasses import dataclass
from enum import Enum


class CommandName(Enum):
    SET_VARIABLE = "SET_VARIABLE"

    STEP = "STEP"
    CONTINUE = "CONTINUE"
    QUIT = "QUIT"


@dataclass(frozen=True)
class Command:
    name: CommandName
    args: list[str]

    @classmethod
    async def from_string(cls, raw_command: str) -> "Command":
        parts = raw_command.strip().split()
        if not parts:
            raise ValueError("Empty command")

        name_str, name = parts[0], None
        args = parts[1:]

        try:
            name = CommandName(name_str)
        except ValueError:
            raise ValueError(f"Invalid command: {name_str}")

        return Command(name, args)
