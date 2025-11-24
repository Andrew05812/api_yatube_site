# Инструкция по настройке Docker и CI/CD для Kittygram

## Структура проекта

Проект настроен для работы в Docker контейнерах со следующей структурой:

- `backend` - Django приложение (контейнер `backend`)
- `frontend` - React приложение (контейнер `frontend`)
- `gateway` - Nginx reverse proxy (контейнер `gateway`)
- `db` - PostgreSQL база данных (контейнер `db`)

## Volumes

Проект использует следующие volumes:

- `static_volume` - для статических файлов Django и React
- `media_volume` - для медиа файлов (изображения котиков)
- `pg_data` - для данных PostgreSQL

## Запуск проекта

1. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

2. Отредактируйте `.env` файл, установив необходимые значения:
- `SECRET_KEY` - секретный ключ Django
- `POSTGRES_PASSWORD` - пароль для PostgreSQL
- И другие переменные окружения

3. Запустите контейнеры:
```bash
docker-compose up -d
```

4. Приложение будет доступно по адресу: http://localhost

## Настройка GitHub Actions

Для работы CI/CD необходимо настроить следующие secrets в GitHub:

1. `DOCKER_USERNAME` - ваш логин на Docker Hub
2. `DOCKER_PASSWORD` - ваш пароль или access token на Docker Hub
3. `TELEGRAM_TOKEN` - токен Telegram бота (получить у @BotFather)
4. `TELEGRAM_TO` - ваш Telegram chat ID (можно получить у @userinfobot)

### Как получить Telegram токен:

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### Как получить Telegram chat ID:

1. Найдите @userinfobot в Telegram
2. Отправьте команду `/start`
3. Бот вернет ваш chat ID

## Образы Docker Hub

После успешного выполнения workflow, следующие образы будут загружены на Docker Hub:

- `username/kittygram_backend:latest`
- `username/kittygram_frontend:latest`
- `username/kittygram_gateway:latest`

Где `username` - ваш логин на Docker Hub из секрета `DOCKER_USERNAME`.

## Тестирование

Workflow выполняет следующие проверки:

1. **Backend тесты:**
   - Проверка кода с помощью `ruff`
   - Запуск Django тестов

2. **Frontend тесты:**
   - Запуск React тестов

3. **Сборка и загрузка:**
   - Сборка всех Docker образов
   - Загрузка образов на Docker Hub
   - Отправка уведомления в Telegram

## Структура файлов

```
kittygram_backend-main/
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions workflow
├── .dockerignore             # Игнорируемые файлы для Docker
├── Dockerfile                # Dockerfile для backend
├── docker-compose.yml        # Конфигурация Docker Compose
├── env.example               # Пример переменных окружения
├── requirements.txt          # Python зависимости
├── nginx/
│   ├── Dockerfile           # Dockerfile для gateway
│   └── nginx.conf           # Конфигурация Nginx
└── frontend/
    ├── Dockerfile           # Dockerfile для frontend
    └── .dockerignore        # Игнорируемые файлы для Docker
```

