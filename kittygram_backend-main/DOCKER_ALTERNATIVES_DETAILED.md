# Подробное руководство по альтернативам Docker Desktop

## Вариант 1: Podman (Рекомендуется для Windows)

### Что такое Podman?
Podman - это альтернатива Docker, которая:
- **Не требует виртуальных машин** (работает нативно в Windows)
- **Совместим с Docker** (использует те же команды и файлы)
- **Не конфликтует с другими виртуальными машинами**
- **Бесплатный и open-source**

### Установка Podman на Windows

#### Шаг 1: Установка Podman Desktop

1. Скачайте установщик с официального сайта:
   - Перейдите на https://podman-desktop.io/
   - Нажмите "Download for Windows"
   - Скачайте `.exe` файл

2. Запустите установщик:
   - Дважды кликните на скачанный файл
   - Следуйте инструкциям установщика
   - Примите лицензионное соглашение
   - Выберите путь установки (можно оставить по умолчанию)
   - Дождитесь завершения установки

3. Запустите Podman Desktop:
   - После установки запустите Podman Desktop из меню Пуск
   - При первом запуске может потребоваться перезагрузка компьютера

#### Шаг 2: Установка podman-compose

Podman Desktop включает Podman, но для работы с `docker-compose.yml` нужен `podman-compose`:

**Вариант A: Через pip (Python должен быть установлен)**
```bash
pip install podman-compose
```

**Вариант B: Через pipx (рекомендуется)**
```bash
# Установите pipx, если его нет
python -m pip install --user pipx
python -m pipx ensurepath

# Установите podman-compose
pipx install podman-compose
```

**Вариант C: Через Chocolatey (если установлен)**
```bash
choco install podman-compose
```

#### Шаг 3: Настройка проекта

1. Убедитесь, что Podman Desktop запущен

2. Создайте файл `.env` (если еще не создан):
```bash
cd kittygram_backend-main
bash create_env.sh
# или создайте вручную (см. инструкции выше)
```

3. Замените команды Docker на Podman:

**Способ 1: Использовать podman-compose напрямую**
```bash
podman-compose up -d
```

**Способ 2: Создать алиасы (удобнее)**
Добавьте в ваш `.bashrc` или `.zshrc`:
```bash
alias docker='podman'
alias docker-compose='podman-compose'
```

После этого можно использовать обычные команды:
```bash
docker-compose up -d
docker ps
docker-compose down
```

#### Шаг 4: Запуск проекта

```bash
cd kittygram_backend-main
podman-compose up -d
```

Проверка статуса:
```bash
podman-compose ps
# или
podman ps
```

Просмотр логов:
```bash
podman-compose logs -f
```

Остановка:
```bash
podman-compose down
```

### Преимущества Podman:
- ✅ Не требует виртуальных машин
- ✅ Не конфликтует с VirtualBox/VMware
- ✅ Полная совместимость с Docker
- ✅ Меньше потребление ресурсов
- ✅ Безопаснее (rootless режим)

### Недостатки:
- ⚠️ Некоторые продвинутые функции Docker могут не работать
- ⚠️ Нужна дополнительная установка podman-compose

---

## Вариант 3: Colima

### Что такое Colima?
Colima (Containers on Linux on Mac/Windows) - это инструмент для запуска Docker без Docker Desktop:
- Использует виртуальную машину Linux (но более легковесную)
- Работает через WSL2 или QEMU
- Может конфликтовать с другими VM, но менее вероятно

### Установка Colima на Windows

#### Шаг 1: Установка WSL2 (если еще не установлен)

1. Откройте PowerShell от имени администратора:
```powershell
wsl --install
```

2. Перезагрузите компьютер

3. После перезагрузки WSL2 будет установлен автоматически

#### Шаг 2: Установка Colima

**Через Homebrew (если установлен):**
```bash
brew install colima docker docker-compose
```

**Через Chocolatey:**
```bash
choco install colima
```

**Вручную (через WSL2):**
```bash
# В WSL2 терминале
curl -LO "https://github.com/abiosoft/colima/releases/latest/download/colima-Linux-x86_64"
sudo mv colima-Linux-x86_64 /usr/local/bin/colima
sudo chmod +x /usr/local/bin/colima
```

#### Шаг 3: Установка Docker CLI для Windows

Colima запускает Docker daemon в VM, но нужен клиент на Windows:

1. Скачайте Docker CLI:
   - Перейдите на https://github.com/docker/cli/releases
   - Скачайте `docker.exe` для Windows

2. Или установите через Chocolatey:
```bash
choco install docker-cli
```

#### Шаг 4: Настройка Colima

1. Запустите Colima:
```bash
colima start
```

При первом запуске Colima:
- Создаст виртуальную машину Linux
- Установит Docker внутри VM
- Настроит сеть

2. Проверьте статус:
```bash
colima status
```

3. Настройте Docker клиент для работы с Colima:
```bash
# Colima автоматически настроит переменные окружения
# Но можно проверить:
export DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"
```

#### Шаг 5: Использование с проектом

```bash
cd kittygram_backend-main

# Убедитесь, что Colima запущен
colima status

# Запустите проект
docker-compose up -d
```

### Управление Colima

```bash
# Запуск
colima start

# Остановка
colima stop

# Перезапуск
colima restart

# Удаление VM
colima delete

# Просмотр логов
colima logs
```

### Настройка ресурсов Colima

Создайте файл `~/.colima/default/colima.yaml`:
```yaml
cpu: 4
memory: 8
disk: 60
```

Затем перезапустите:
```bash
colima stop
colima start
```

### Преимущества Colima:
- ✅ Полная совместимость с Docker
- ✅ Не требует Docker Desktop
- ✅ Легковеснее Docker Desktop
- ✅ Хорошо работает с WSL2

### Недостатки:
- ⚠️ Все еще использует виртуальную машину (может конфликтовать)
- ⚠️ Требует WSL2
- ⚠️ Более сложная настройка

---

## Вариант 4: Локальный запуск без Docker

### Полная настройка для локальной разработки

Этот вариант позволяет запустить проект без контейнеров, используя локальные сервисы.

#### Шаг 1: Установка PostgreSQL

**Windows:**

1. Скачайте PostgreSQL:
   - Перейдите на https://www.postgresql.org/download/windows/
   - Скачайте установщик

2. Установите PostgreSQL:
   - Запустите установщик
   - Запомните пароль для пользователя `postgres`
   - Порт по умолчанию: `5432`

3. Создайте базу данных:
```sql
-- Откройте pgAdmin или psql
CREATE DATABASE kittygram;
CREATE USER kittygram_user WITH PASSWORD 'kittygram_password';
GRANT ALL PRIVILEGES ON DATABASE kittygram TO kittygram_user;
```

**Альтернатива: Использовать SQLite (проще, но не для production)**

Если не хотите устанавливать PostgreSQL, можно использовать SQLite для разработки.

#### Шаг 2: Настройка Backend (Django)

1. Перейдите в директорию проекта:
```bash
cd kittygram_backend-main
```

2. Создайте виртуальное окружение:
```bash
python -m venv env
```

3. Активируйте виртуальное окружение:

**Windows (Git Bash):**
```bash
source env/Scripts/activate
```

**Windows (PowerShell):**
```powershell
.\env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
env\Scripts\activate.bat
```

4. Установите зависимости:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. Создайте файл `.env` для локальной разработки:
```bash
cat > .env << 'EOF'
SECRET_KEY=!uxdbzq5b)pd+egyymtkfy=gm1!hdoz7#37muy@u)+tmtwxi8v
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Для PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=kittygram
POSTGRES_USER=kittygram_user
POSTGRES_PASSWORD=kittygram_password
DB_HOST=localhost
DB_PORT=5432

# Или для SQLite (проще для начала)
# DB_ENGINE=django.db.backends.sqlite3
EOF
```

6. Обновите `settings.py` для работы с локальной БД:

Файл уже настроен, но убедитесь, что переменные окружения читаются правильно.

7. Выполните миграции:
```bash
python manage.py migrate
```

8. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

9. Соберите статические файлы:
```bash
python manage.py collectstatic --noinput
```

10. Запустите сервер разработки:
```bash
python manage.py runserver
```

Backend будет доступен по адресу: http://127.0.0.1:8000

#### Шаг 3: Настройка Frontend (React)

1. Перейдите в директорию frontend:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. Создайте файл `.env` для frontend (если нужен):
```bash
cat > .env << 'EOF'
REACT_APP_API_URL=http://127.0.0.1:8000
EOF
```

4. Запустите dev сервер:
```bash
npm start
```

Frontend будет доступен по адресу: http://localhost:3000

#### Шаг 4: Настройка Nginx (опционально, для production-like окружения)

Если хотите использовать Nginx локально:

1. Установите Nginx для Windows:
   - Скачайте с http://nginx.org/en/download.html
   - Распакуйте в `C:\nginx`

2. Обновите `nginx/nginx.conf`:
```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name localhost;

    client_max_body_size 20M;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Запустите Nginx:
```bash
cd C:\nginx
start nginx
```

### Упрощенный вариант без Nginx

Можно запустить только backend и frontend отдельно:

**Терминал 1 (Backend):**
```bash
cd kittygram_backend-main
source env/Scripts/activate
python manage.py runserver
```

**Терминал 2 (Frontend):**
```bash
cd kittygram_backend-main/frontend
npm start
```

Затем:
- Backend API: http://127.0.0.1:8000
- Frontend: http://localhost:3000
- Frontend будет проксировать запросы к API автоматически

### Скрипты для автоматизации

Создайте файл `start_local.bat` для Windows:
```batch
@echo off
echo Starting Kittygram locally...

echo Starting Backend...
start "Backend" cmd /k "cd kittygram_backend-main && env\Scripts\activate && python manage.py runserver"

timeout /t 3

echo Starting Frontend...
start "Frontend" cmd /k "cd kittygram_backend-main\frontend && npm start"

echo Both servers are starting...
pause
```

Или `start_local.sh` для Git Bash:
```bash
#!/bin/bash
echo "Starting Kittygram locally..."

# Start Backend
cd kittygram_backend-main
source env/Scripts/activate
python manage.py runserver &
BACKEND_PID=$!

# Wait a bit
sleep 3

# Start Frontend
cd frontend
npm start &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
wait
```

### Преимущества локального запуска:
- ✅ Не требует Docker или виртуальных машин
- ✅ Полный контроль над окружением
- ✅ Быстрее для разработки (hot reload)
- ✅ Легче отлаживать

### Недостатки:
- ⚠️ Нужно устанавливать все зависимости вручную
- ⚠️ Настройка сложнее
- ⚠️ Окружение может отличаться от production
- ⚠️ Нужно запускать несколько процессов вручную

---

## Сравнение вариантов

| Критерий | Podman | Colima | Локальный запуск |
|---------|--------|--------|------------------|
| Конфликт с VM | ❌ Нет | ⚠️ Возможен | ❌ Нет |
| Сложность установки | ⭐⭐ Средняя | ⭐⭐⭐ Сложная | ⭐⭐⭐⭐ Очень сложная |
| Совместимость с Docker | ✅ 100% | ✅ 100% | ❌ Нет |
| Производительность | ⭐⭐⭐⭐ Высокая | ⭐⭐⭐ Средняя | ⭐⭐⭐⭐ Высокая |
| Ресурсы | ⭐⭐⭐⭐ Низкие | ⭐⭐⭐ Средние | ⭐⭐⭐⭐ Низкие |
| Подходит для CI/CD | ✅ Да | ✅ Да | ❌ Нет |

## Рекомендация

Для вашей ситуации (конфликт с виртуальными машинами) лучше всего подойдет **Podman (Вариант 1)**, так как:
- Не использует виртуальные машины
- Полная совместимость с Docker
- Проще в установке, чем Colima
- Подходит для CI/CD

Если Podman не подходит, используйте **Локальный запуск (Вариант 4)** для разработки, а для CI/CD используйте GitHub Actions (который уже настроен в проекте).

