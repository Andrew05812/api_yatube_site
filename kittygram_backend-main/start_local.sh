#!/bin/bash

# Скрипт для локального запуска Kittygram без Docker

echo "🚀 Запуск Kittygram локально..."

# Проверка Python
if ! command -v python &> /dev/null; then
    echo "❌ Python не найден. Установите Python 3.9+"
    exit 1
fi

# Проверка Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Установите Node.js 18+"
    exit 1
fi

# Создание виртуального окружения, если его нет
if [ ! -d "env" ]; then
    echo "📦 Создание виртуального окружения..."
    python -m venv env
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source env/Scripts/activate

# Установка зависимостей Python
echo "📥 Установка Python зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание .env для локальной разработки (если не существует)
if [ ! -f ".env" ]; then
    echo "📝 Создание .env файла..."
    cat > .env << 'EOF'
SECRET_KEY=!uxdbzq5b)pd+egyymtkfy=gm1!hdoz7#37muy@u)+tmtwxi8v
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Используем SQLite для простоты (можно заменить на PostgreSQL)
DB_ENGINE=django.db.backends.sqlite3
EOF
fi

# Выполнение миграций
echo "🗄️  Выполнение миграций базы данных..."
python manage.py migrate

# Создание суперпользователя (опционально)
echo "👤 Хотите создать суперпользователя? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Сборка статических файлов
echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput

# Запуск backend в фоне
echo "🔵 Запуск Django backend..."
python manage.py runserver &
BACKEND_PID=$!

# Ожидание запуска backend
sleep 3

# Переход в директорию frontend
cd frontend || exit

# Установка зависимостей Node.js
if [ ! -d "node_modules" ]; then
    echo "📥 Установка Node.js зависимостей..."
    npm install
fi

# Запуск frontend
echo "🟢 Запуск React frontend..."
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Серверы запущены!"
echo "📡 Backend: http://127.0.0.1:8000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Нажмите Ctrl+C для остановки всех серверов"

# Ожидание прерывания
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

