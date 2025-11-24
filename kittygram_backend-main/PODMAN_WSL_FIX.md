# Решение проблемы WSL с Podman

## Проблема: "WSL import of guest OS failed"

Эта ошибка возникает, когда Podman пытается создать виртуальную машину через WSL2, но встречает проблемы.

## Решение 1: Проверка и обновление WSL2

### Шаг 1: Проверьте версию WSL

Откройте PowerShell от имени администратора и выполните:

```powershell
wsl --version
```

Если команда не работает, значит WSL2 не установлен или установлена старая версия.

### Шаг 2: Обновите WSL2

```powershell
# Обновите WSL до последней версии
wsl --update

# Установите WSL2 по умолчанию
wsl --set-default-version 2
```

### Шаг 3: Перезагрузите компьютер

После обновления WSL2 перезагрузите компьютер.

### Шаг 4: Проверьте установленные дистрибутивы

```powershell
wsl --list --verbose
```

Должен быть хотя бы один дистрибутив с версией 2.

## Решение 2: Установка WSL2 с дистрибутивом

Если WSL2 не установлен:

```powershell
# Установите WSL2 с Ubuntu
wsl --install

# Или установите вручную
wsl --install -d Ubuntu
```

После установки перезагрузите компьютер.

## Решение 3: Использование альтернативного бэкенда Podman

Podman может использовать QEMU вместо WSL2. Попробуйте:

### Вариант A: Настройка Podman на использование QEMU

1. Откройте Podman Desktop
2. Перейдите в Settings → Resources → Machines
3. При создании машины выберите "QEMU" вместо "WSL2" (если доступно)

### Вариант B: Создание машины через командную строку с QEMU

```bash
podman machine init --rootful
```

Или попробуйте без rootful:

```bash
podman machine init
```

## Решение 4: Очистка и пересоздание

Если машина была создана некорректно:

```bash
# Удалите все машины Podman
podman machine rm -f podman-machine-default

# Очистите директорию (осторожно!)
# Удалите: C:\Users\Andre\.local\share\containers\podman\machine

# Создайте машину заново
podman machine init
podman machine start
```

## Решение 5: Использование локального запуска (БЕЗ Docker/Podman)

Если проблемы с WSL2 продолжаются, лучше использовать локальный запуск без контейнеров.

### Быстрый переход на локальный запуск:

1. **Установите PostgreSQL локально** (или используйте SQLite для разработки)

2. **Настройте Backend:**
```bash
cd kittygram_backend-main

# Создайте виртуальное окружение
python -m venv env

# Активируйте (в Git Bash)
source env/Scripts/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте .env для локальной разработки
cat > .env << 'EOF'
SECRET_KEY=!uxdbzq5b)pd+egyymtkfy=gm1!hdoz7#37muy@u)+tmtwxi8v
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Для SQLite (проще для начала)
DB_ENGINE=django.db.backends.sqlite3
EOF

# Выполните миграции
python manage.py migrate

# Запустите сервер
python manage.py runserver
```

3. **Настройте Frontend:**
```bash
cd frontend
npm install
npm start
```

## Решение 6: Использование Colima (альтернатива)

Если WSL2 не работает, попробуйте Colima, который может использовать QEMU напрямую:

1. Установите Colima (см. DOCKER_ALTERNATIVES_DETAILED.md)
2. Colima может работать без WSL2, используя QEMU

## Рекомендация

Учитывая, что у вас конфликт с виртуальными машинами и проблемы с WSL2, **лучше всего использовать локальный запуск (Решение 5)**.

Это позволит:
- ✅ Избежать проблем с виртуальными машинами
- ✅ Быстрее разрабатывать (hot reload)
- ✅ Не зависеть от Docker/Podman
- ✅ Легче отлаживать

Для CI/CD используйте GitHub Actions (уже настроен), который будет запускать Docker в облаке.

## Проверка после исправления

После применения любого решения проверьте:

```bash
# Для Podman
podman machine list
podman ps

# Для WSL2
wsl --list --verbose
```

