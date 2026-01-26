from pathlib import Path
from shutil import copy
from tempfile import gettempdir
from uuid import UUID

from app.common.app_config import app_config


async def handle_debugging_start(uuid: UUID) -> None:
    await copy_python_code_wrapper(uuid)


async def copy_python_code_wrapper(uuid: UUID) -> None:
    python_code_wrapper_path = app_config.RESOURCES_PATH / "python_code_wrapper.py"
    target_path = Path(gettempdir()).resolve() / "postdb" / str(uuid)

    copy(python_code_wrapper_path, target_path)
