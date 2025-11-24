@echo off
REM Скрипт для локального запуска Kittygram без Docker (Windows)

echo 🚀 Запуск Kittygram локально...

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден. Установите Python 3.9+
    pause
    exit /b 1
)

REM Проверка Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js не найден. Установите Node.js 18+
    pause
    exit /b 1
)

REM Создание виртуального окружения, если его нет
if not exist "env" (
    echo 📦 Создание виртуального окружения...
    python -m venv env
)

REM Активация виртуального окружения
echo 🔧 Активация виртуального окружения...
call env\Scripts\activate.bat

REM Установка зависимостей Python
echo 📥 Установка Python зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Создание .env для локальной разработки (если не существует)
if not exist ".env" (
    echo 📝 Создание .env файла...
    (
        echo SECRET_KEY=!uxdbzq5b)pd+egyymtkfy=gm1!hdoz7#37muy@u)+tmtwxi8v
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Используем SQLite для простоты
        echo DB_ENGINE=django.db.backends.sqlite3
    ) > .env
)

REM Выполнение миграций
echo 🗄️  Выполнение миграций базы данных...
python manage.py migrate

REM Сборка статических файлов
echo 📦 Сборка статических файлов...
python manage.py collectstatic --noinput

REM Запуск backend
echo 🔵 Запуск Django backend...
start "Backend" cmd /k "python manage.py runserver"

REM Ожидание запуска backend
timeout /t 3 /nobreak >nul

REM Переход в директорию frontend
cd frontend

REM Установка зависимостей Node.js
if not exist "node_modules" (
    echo 📥 Установка Node.js зависимостей...
    call npm install
)

REM Запуск frontend
echo 🟢 Запуск React frontend...
start "Frontend" cmd /k "npm start"

echo.
echo ✅ Серверы запущены!
echo 📡 Backend: http://127.0.0.1:8000
echo 🌐 Frontend: http://localhost:3000
echo.
echo Закройте окна командной строки для остановки серверов
pause

