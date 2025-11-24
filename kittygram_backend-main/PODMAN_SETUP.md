# Пошаговая инструкция по установке и запуску Podman

## Шаг 1: Установка Podman Desktop

1. **Запустите установщик Podman Desktop**
   - Найдите скачанный файл (обычно `Podman-Desktop-Setup-x.x.x.exe`)
   - Дважды кликните на него
   - Если появится предупреждение безопасности, нажмите "Дополнительно" → "Выполнить в любом случае"

2. **Следуйте инструкциям установщика:**
   - Примите лицензионное соглашение
   - Выберите путь установки (можно оставить по умолчанию)
   - Нажмите "Install"
   - Дождитесь завершения установки

3. **Запустите Podman Desktop:**
   - После установки запустите Podman Desktop из меню Пуск
   - При первом запуске может потребоваться перезагрузка компьютера
   - Если система просит перезагрузить - сделайте это

4. **Проверьте, что Podman запущен:**
   - Откройте Podman Desktop
   - В левом нижнем углу должно быть написано "Podman machine is running" (зеленый индикатор)
   - Если не запущен - нажмите кнопку "Start" или "Play"

## Шаг 2: Установка podman-compose

Откройте Git Bash или PowerShell и выполните одну из команд:

**Вариант A: Через pip (если Python установлен)**
```bash
pip install podman-compose
```

**Вариант B: Через pipx (рекомендуется)**
```bash
# Установите pipx, если его нет
python -m pip install --user pipx
python -m pipx ensurepath

# Перезапустите терминал, затем:
pipx install podman-compose
```

**Вариант C: Через Chocolatey (если установлен)**
```bash
choco install podman-compose
```

**Проверьте установку:**
```bash
podman-compose --version
```

Должна вывестись версия, например: `podman-compose version 1.0.x`

## Шаг 3: Создание файла .env

Перейдите в директорию проекта и создайте файл `.env`:

```bash
cd kittygram_backend-main
bash create_env.sh
```

Или создайте вручную:

```bash
cat > .env << 'EOF'
SECRET_KEY=!uxdbzq5b)pd+egyymtkfy=gm1!hdoz7#37muy@u)+tmtwxi8v
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL settings
POSTGRES_DB=kittygram
POSTGRES_USER=kittygram_user
POSTGRES_PASSWORD=kittygram_password

# Django database settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=kittygram
DB_HOST=db
DB_PORT=5432
EOF
```

Проверьте, что файл создан:
```bash
ls -la .env
cat .env
```

## Шаг 4: Проверка Podman

Убедитесь, что Podman работает:

```bash
podman --version
podman ps
```

Если команды работают без ошибок - все готово!

## Шаг 5: Запуск проекта

Теперь можно запустить проект:

```bash
cd kittygram_backend-main
podman-compose up -d
```

Эта команда:
- Соберет все образы (backend, frontend, gateway)
- Создаст контейнеры
- Запустит их в фоновом режиме

**Проверка статуса:**
```bash
podman-compose ps
```

Должны быть запущены 4 контейнера:
- `db` (PostgreSQL)
- `backend` (Django)
- `frontend` (React)
- `gateway` (Nginx)

**Просмотр логов:**
```bash
podman-compose logs -f
```

Для просмотра логов конкретного сервиса:
```bash
podman-compose logs backend
podman-compose logs frontend
```

## Шаг 6: Доступ к приложению

После успешного запуска приложение будет доступно по адресу:
- **http://localhost** - основное приложение через gateway
- **http://localhost:8000** - backend API (если нужен прямой доступ)

## Полезные команды

**Остановка контейнеров:**
```bash
podman-compose stop
```

**Остановка и удаление контейнеров:**
```bash
podman-compose down
```

**Перезапуск:**
```bash
podman-compose restart
```

**Пересборка образов (после изменений в коде):**
```bash
podman-compose up -d --build
```

**Просмотр всех контейнеров Podman:**
```bash
podman ps -a
```

**Просмотр образов:**
```bash
podman images
```

## Создание алиасов (опционально)

Если хотите использовать команды `docker` и `docker-compose` вместо `podman` и `podman-compose`, добавьте алиасы в ваш `.bashrc`:

```bash
echo 'alias docker="podman"' >> ~/.bashrc
echo 'alias docker-compose="podman-compose"' >> ~/.bashrc
source ~/.bashrc
```

После этого можно использовать:
```bash
docker-compose up -d
docker ps
```

## Решение проблем

### Проблема: "podman-compose: command not found"
**Решение:** Убедитесь, что `podman-compose` установлен и находится в PATH. Попробуйте:
```bash
python -m pip install --user podman-compose
```

### Проблема: "Podman machine is not running"
**Решение:** 
1. Откройте Podman Desktop
2. Нажмите кнопку "Start" или "Play"
3. Дождитесь запуска машины

### Проблема: "Error: cannot connect to Podman"
**Решение:**
1. Проверьте, что Podman Desktop запущен
2. Перезапустите Podman Desktop
3. Проверьте: `podman ps`

### Проблема: Порты заняты
**Решение:**
Если порт 80 занят, измените в `docker-compose.yml`:
```yaml
gateway:
  ports:
    - "8080:80"  # Используйте другой порт
```

Тогда приложение будет доступно по адресу http://localhost:8080

## Следующие шаги

После успешного запуска:
1. ✅ Проект работает в контейнерах
2. ✅ Можно тестировать функциональность
3. ✅ Можно делать изменения в коде
4. ✅ Для обновления после изменений: `podman-compose up -d --build`

Для настройки CI/CD с GitHub Actions - все уже готово! Просто настройте secrets в GitHub (см. DOCKER_SETUP.md).

