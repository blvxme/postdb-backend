from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    RESOURCES_PATH = Path(__file__).resolve().parent.parent.parent / "resources"


app_config = AppConfig()
