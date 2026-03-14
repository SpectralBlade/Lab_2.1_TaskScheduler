from pathlib import Path
from src.sources import ApiSource, GeneratorSource, FileSource

CURRENT_DIR = Path(__file__).parent
JSON_PATH = CURRENT_DIR / 'example.json'

EXAMPLE_SOURCES = [
    GeneratorSource(10),
    ApiSource('https://i_love_samir_akhmed.com', 3),
    FileSource(str(JSON_PATH))
]