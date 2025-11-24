# Быстрый запуск без Docker

## Проблема с виртуализацией

Если у вас ошибка "WSL2 не поддерживается" или конфликт с виртуальными машинами, используйте локальный запуск.

## Пошаговая инструкция

### Шаг 1: Перейдите в правильную директорию

```bash
cd kittygram_backend-main
```

### Шаг 2: Запустите автоматический скрипт

**В Git Bash:**
```bash
bash start_local.sh
```

**Или в CMD/PowerShell:**
```cmd
start_local.bat
```

### Шаг 3: Ручной запуск (если скрипт не работает)

#### Терминал 1 - Backend:

```bash
cd kittygram_backend-main

# Активируйте виртуальное окружение
source env/Scripts/activate

# Если окружения нет - создайте
python -m venv env
source env/Scripts/activate

# Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Создайте .env
cat > .env << 'EOF'
SECRET_KEY=!uxdbzq5b)pd+egyymtkfy=gm1!hdoz7#37muy@u)+tmtwxi8v
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
EOF

# Миграции
python manage.py migrate

# Запуск сервера
python manage.py runserver
```

#### Терминал 2 - Frontend:

```bash
cd kittygram_backend-main/frontend

# Установите зависимости (если еще не установлены)
npm install

# Запуск
npm start
```

## Доступ к приложению

После запуска:
- **Backend API**: http://127.0.0.1:8000
- **Frontend**: http://localhost:3000
- **Admin панель**: http://127.0.0.1:8000/admin

## Создание суперпользователя

```bash
cd kittygram_backend-main
source env/Scripts/activate
python manage.py createsuperuser
```

## Остановка серверов

Нажмите `Ctrl+C` в каждом терминале, где запущены серверы.

