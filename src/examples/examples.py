from pathlib import Path
from src.sources import ApiSource, GeneratorSource, FileSource

"""
Модуль содержит примеры конфигураций различных источников задач.
Используется в качестве входных данных для демонстрации работы 
валидатора и планировщика задач.
"""

CURRENT_DIR = Path(__file__).parent
JSON_PATH = CURRENT_DIR / 'example.json'

SOURCES = [
    GeneratorSource(10),
    ApiSource('https://i_love_samir_akhmed.com', 3),
    FileSource(str(JSON_PATH))
]