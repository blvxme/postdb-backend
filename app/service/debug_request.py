from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from dataclasses import dataclass
from os import makedirs
from pathlib import Path
from shutil import copy
from tempfile import gettempdir
from uuid import UUID, uuid4

from app.common.app_config import app_config

from app.service.python_code_context import python_code_context


@dataclass(frozen=True)
class TranslatorOutput:
    return_code: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class CodeInfo:
    states_by_process: dict[str, list[str]]
    value_by_input_variable: dict[str, str]
    value_by_output_variable: dict[str, str]


async def handle_debug_request(post_code: str) -> tuple[UUID, TranslatorOutput, CodeInfo]:
    uuid = uuid4()
    translation_path = prepare_translation_path(uuid)
    translator_return_code, translator_stdout, translator_stderr = await translate_post_code(
        post_code,
        translation_path
    )

    states_by_process = extract_states_by_process(translation_path)
    value_by_input_variable = extract_value_by_input_variable(translation_path)
    value_by_output_variable = extract_value_by_output_variable(translation_path)

    return (
        uuid,
        TranslatorOutput(translator_return_code, translator_stdout, translator_stderr),
        CodeInfo(states_by_process, value_by_input_variable, value_by_output_variable)
    )


def prepare_translation_path(uuid: UUID) -> Path:
    postdb_path = Path(gettempdir()).resolve() / "postdb"
    makedirs(postdb_path, exist_ok=True)

    post2py_path = app_config.RESOURCES_PATH / "post2py.jar"
    copy(post2py_path, postdb_path)

    translation_path = postdb_path / str(uuid)
    makedirs(translation_path)

    mute_types_path = app_config.RESOURCES_PATH / "MuteTypes.py"
    copy(mute_types_path, translation_path)

    return translation_path


async def translate_post_code(post_code: str, translation_path: Path) -> tuple[int, str, str]:
    post_code_path = translation_path / "post_code.post"
    with open(post_code_path, "w", encoding="utf-8") as f:
        f.write(post_code)

    translator_path = translation_path.parent / "post2py.jar"
    python_code_path = translation_path / "python_code.py"

    process = await create_subprocess_exec(
        "java", "-jar", str(translator_path), str(post_code_path), f"-o={python_code_path.name}",
        cwd=translation_path,
        stdout=PIPE,
        stderr=PIPE
    )

    stdout_bytes, stderr_bytes = await process.communicate()

    stdout = stdout_bytes.decode("utf-8") if stdout_bytes else ""
    stderr = stderr_bytes.decode("utf-8") if stderr_bytes else ""
    return_code = process.returncode if process.returncode is not None else -1

    return return_code, stdout, stderr


def extract_states_by_process(translation_path: Path) -> dict[str, list[str]]:
    states_by_process: dict[str, list[str]] = {}

    with python_code_context(translation_path) as module:
        processes = getattr(module, "processesDict", {})

        for process_name, process_instance in processes.items():
            states = getattr(process_instance, "States", None)
            if states is None:
                states = getattr(process_instance.__class__, "States", None)
                if states is None:
                    states_by_process[process_name] = []
                    continue

            try:
                members = list(states)
                states_by_process[process_name] = [m.name for m in members]
            except Exception:
                states_by_process[process_name] = list(getattr(states, "__members__", {}).keys())

    return states_by_process


def extract_value_by_input_variable(translation_path: Path) -> dict[str, str]:
    value_by_input_variable: dict[str, str] = {}

    with python_code_context(translation_path) as module:
        input_variables = getattr(module, "inVars", {})

        for variable_name, variable_value in input_variables.items():
            value_by_input_variable[variable_name] = str(variable_value).lower()

    return value_by_input_variable


def extract_value_by_output_variable(translation_path: Path) -> dict[str, str]:
    value_by_output_variable: dict[str, str] = {}

    with python_code_context(translation_path) as module:
        output_variables = getattr(module, "outVars", {})

        for variable_name, variable_value in output_variables.items():
            value_by_output_variable[variable_name] = str(variable_value).lower()

    return value_by_output_variable
