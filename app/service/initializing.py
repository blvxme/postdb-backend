from uuid import UUID

from app.settings import settings


class DebuggingInitializer:
    async def initialize(self, uuid: UUID) -> None:
        await self._add_debugging_addition(uuid)

    async def _add_debugging_addition(self, uuid: UUID) -> None:
        addition_content = None

        addition_path = settings.RESOURCES_PATH / "python_code_addition.py"
        with open(addition_path, "r", encoding="utf-8") as f:
            addition_content = f.read()

        python_code_path = settings.TRANSLATION_PATH / str(uuid) / "python_code.py"
        with open(python_code_path, "a", encoding="utf-8") as f:
            f.write(addition_content)


debugging_initializer = DebuggingInitializer()
