import shutil
import os
from pathlib import Path

# Получаем родительскую директорию
base_dir = Path(__file__).parent.parent
source = base_dir / "kittygram_frontend-main"
dest = base_dir / "kittygram_backend-main" / "frontend"

if source.exists():
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    print(f"Скопировано из {source} в {dest}")
else:
    print(f"Источник {source} не найден")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Содержимое родительской директории: {list(base_dir.iterdir())}")

