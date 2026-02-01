from pathlib import Path
from tempfile import gettempdir
from uuid import UUID

from app.common.app_config import app_config


async def handle_debugging_start(uuid: UUID) -> None:
    await add_debugging_addition(uuid)


async def add_debugging_addition(uuid: UUID) -> None:
    addition_content = None

    addition_path = app_config.RESOURCES_PATH / "python_code_addition.py"
    with open(addition_path, "r", encoding="utf-8") as f:
        addition_content = f.read()

    python_code_path = Path(gettempdir()).resolve() / "postdb" / str(uuid) / "python_code.py"
    with open(python_code_path, "a", encoding="utf-8") as f:
        f.write(addition_content)
