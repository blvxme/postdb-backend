from contextlib import contextmanager
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from sys import path
from types import ModuleType
from typing import Iterator


@contextmanager
def python_code_context(translation_path: Path) -> Iterator[ModuleType]:
    spec = spec_from_file_location(translation_path.name, translation_path / "python_code.py")
    if spec is None:
        raise ImportError(f"Unable to load spec for {translation_path}")
    elif spec.loader is None:
        raise ImportError(f"Spec loader is missing for {translation_path}")

    module = module_from_spec(spec)

    path.insert(0, str(translation_path))

    try:
        spec.loader.exec_module(module)
        yield module
    finally:
        path.pop(0)
