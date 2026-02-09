from dataclasses import dataclass
from pathlib import Path
from tempfile import gettempdir


@dataclass
class Config:
    RESOURCES_PATH = Path(__file__).resolve().parent.parent / "resources"
    TRANSLATION_PATH = Path(gettempdir()).resolve() / "postdb"


config = Config()
