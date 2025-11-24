import shutil
import os
from pathlib import Path

# Получаем абсолютный путь к текущему файлу и поднимаемся на уровень выше
script_dir = Path(__file__).parent
base_dir = script_dir.parent

source = base_dir / "kittygram_frontend-main"
dest = script_dir / "frontend"

print(f"Base directory: {base_dir}")
print(f"Source: {source}")
print(f"Destination: {dest}")
print(f"Source exists: {source.exists()}")
print(f"Destination exists: {dest.exists()}")

if source.exists():
    if dest.exists():
        shutil.rmtree(dest)
        print("Removed existing destination")
    shutil.copytree(source, dest)
    print(f"Successfully copied from {source} to {dest}")
else:
    print(f"Source directory {source} not found!")
    print(f"Available directories: {[d.name for d in base_dir.iterdir() if d.is_dir()]}")

