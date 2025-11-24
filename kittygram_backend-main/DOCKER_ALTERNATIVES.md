# Альтернативы Docker Desktop

Если вы не можете использовать Docker Desktop из-за конфликта с виртуальными машинами, есть несколько альтернатив:

## Вариант 1: Docker Engine через WSL2 (Рекомендуется)

Если у вас установлен WSL2, вы можете использовать Docker Engine напрямую:

1. Установите Docker в WSL2:
```bash
# В WSL2 терминале
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

2. Запустите Docker daemon:
```bash
sudo service docker start
```

3. Используйте проект из WSL2:
```bash
cd /mnt/c/Users/Andre/OneDrive/Рабочий\ стол/VUZ/бэкенд/15/my/kittygram/kittygram_backend-main
docker-compose up -d
```

## Вариант 2: Podman (Альтернатива Docker без виртуальных машин)

Podman - это альтернатива Docker, которая не требует виртуальных машин:

1. Установите Podman Desktop: https://podman-desktop.io/

2. Замените команды:
   - `docker` → `podman`
   - `docker-compose` → `podman-compose`

3. Или создайте алиасы:
```bash
alias docker=podman
alias docker-compose=podman-compose
```

## Вариант 3: Colima (Docker без Docker Desktop)

Colima позволяет запускать Docker без Docker Desktop:

1. Установите Colima: https://github.com/abiosoft/colima

2. Запустите Colima:
```bash
colima start
```

3. Используйте Docker как обычно:
```bash
docker-compose up -d
```

## Вариант 4: Запуск без Docker (Локальная разработка)

Если Docker недоступен, можно запустить проект локально:

### Backend:
```bash
# Создайте виртуальное окружение
python -m venv env
source env/bin/activate  # Linux/Mac
# или
env\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Настройте PostgreSQL локально или используйте SQLite
# Обновите settings.py для использования локальной БД

# Запустите миграции
python manage.py migrate

# Запустите сервер
python manage.py runserver
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

### Nginx (опционально):
Установите Nginx локально и используйте конфигурацию из `nginx/nginx.conf`

## Вариант 5: Использование GitHub Actions для тестирования

Для CI/CD можно использовать GitHub Actions, который будет запускать Docker в облаке, даже если локально Docker недоступен.

## Рекомендация

Для вашего случая лучше всего подойдет **Вариант 1 (WSL2)** или **Вариант 2 (Podman)**, так как они не конфликтуют с виртуальными машинами.

