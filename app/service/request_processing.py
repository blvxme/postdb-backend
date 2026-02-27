from asyncio import create_subprocess_exec
from dataclasses import dataclass
from os import makedirs
from pathlib import Path
from shutil import copy
from subprocess import PIPE
from uuid import UUID, uuid4

from app.settings import settings
from app.service.util.context import python_code_context


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


class DebuggingRequestProcessor:
    def __init__(self) -> None:
        self._post_code_translator = PostCodeTranslator()
        self._code_info_extractor = CodeInfoExtractor()

    async def process(self, post_code: str) -> tuple[UUID, TranslatorOutput, CodeInfo]:
        uuid = uuid4()
        translation_path = await self._prepare_translation_path(uuid)
        translator_output = await self._post_code_translator.translate(post_code, translation_path)
        code_info = await self._code_info_extractor.extract(translation_path)
        return uuid, translator_output, code_info

    async def _prepare_translation_path(self, uuid: UUID) -> Path:
        makedirs(settings.TRANSLATION_PATH, exist_ok=True)

        post2py_path = settings.RESOURCES_PATH / "post2py.jar"
        copy(post2py_path, settings.TRANSLATION_PATH)

        translation_path = settings.TRANSLATION_PATH / str(uuid)
        makedirs(translation_path)

        mute_types_path = settings.RESOURCES_PATH / "MuteTypes.py"
        copy(mute_types_path, translation_path)

        return translation_path


class PostCodeTranslator:
    async def translate(self, post_code: str, destination_path: Path) -> TranslatorOutput:
        post_code_path = destination_path / "post_code.post"
        with open(post_code_path, "w", encoding="utf-8") as f:
            f.write(post_code)

        translator_path = settings.TRANSLATION_PATH / "post2py.jar"
        python_code_path = destination_path / "python_code.py"

        process = await create_subprocess_exec(
            "java", "-jar", str(translator_path), str(post_code_path), f"-o={python_code_path.name}",
            cwd=destination_path,
            stdout=PIPE,
            stderr=PIPE
        )

        stdout_bytes, stderr_bytes = await process.communicate()

        stdout = stdout_bytes.decode("utf-8") if stdout_bytes else ""
        stderr = stderr_bytes.decode("utf-8") if stderr_bytes else ""
        return_code = process.returncode if process.returncode is not None else -1

        return TranslatorOutput(return_code, stdout, stderr)


class CodeInfoExtractor:
    async def extract(self, translation_path: Path) -> CodeInfo:
        states_by_process = await self._extract_states_by_process(translation_path)
        value_by_input_variable = await self._extract_value_by_input_variable(translation_path)
        value_by_output_variable = await self._extract_value_by_output_variable(translation_path)
        return CodeInfo(states_by_process, value_by_input_variable, value_by_output_variable)

    async def _extract_states_by_process(self, translation_path: Path) -> dict[str, list[str]]:
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

    async def _extract_value_by_input_variable(self, translation_path: Path) -> dict[str, str]:
        value_by_input_variable: dict[str, str] = {}

        with python_code_context(translation_path) as module:
            input_variables = getattr(module, "inVars", {})

            for variable_name, variable_value in input_variables.items():
                value_by_input_variable[variable_name] = str(variable_value).lower()

        return value_by_input_variable

    async def _extract_value_by_output_variable(self, translation_path: Path) -> dict[str, str]:
        value_by_output_variable: dict[str, str] = {}

        with python_code_context(translation_path) as module:
            output_variables = getattr(module, "outVars", {})

            for variable_name, variable_value in output_variables.items():
                value_by_output_variable[variable_name] = str(variable_value).lower()

        return value_by_output_variable


debugging_request_processor = DebuggingRequestProcessor()
