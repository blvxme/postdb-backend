import dataclasses
import enum


class CommandName(enum.Enum):
    SET_VARIABLE = "SET_VARIABLE"

    STEP = "STEP"
    CONTINUE = "CONTINUE"
    QUIT = "QUIT"


@dataclasses.dataclass(frozen=True)
class Command:
    name: CommandName
    args: list[str]
