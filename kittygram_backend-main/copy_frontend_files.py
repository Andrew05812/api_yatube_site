#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для копирования файлов frontend в структуру backend проекта.
Запустите этот скрипт из директории kittygram_backend-main
"""
import shutil
import os
from pathlib import Path

# Получаем директорию, где находится этот скрипт
script_dir = Path(__file__).parent.absolute()
base_dir = script_dir.parent

source = base_dir / "kittygram_frontend-main"
dest = script_dir / "frontend"

print(f"Рабочая директория: {script_dir}")
print(f"Базовая директория: {base_dir}")
print(f"Источник: {source}")
print(f"Назначение: {dest}")
print(f"Источник существует: {source.exists()}")

if source.exists():
    if dest.exists():
        print("Удаление существующей папки frontend...")
        shutil.rmtree(dest)
    print("Копирование файлов...")
    shutil.copytree(str(source), str(dest))
    print(f"✓ Успешно скопировано из {source} в {dest}")
    print("\nТеперь вы можете:")
    print("1. Перейти в папку frontend: cd frontend")
    print("2. Установить зависимости: npm install")
    print("3. Запустить frontend: npm start")
else:
    print(f"✗ Исходная директория не найдена: {source}")
    print(f"\nДоступные директории в {base_dir}:")
    for item in base_dir.iterdir():
        if item.is_dir():
            print(f"  - {item.name}/")

