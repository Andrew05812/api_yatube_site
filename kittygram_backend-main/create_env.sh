#!/bin/bash

# Создание файла .env для Docker Compose

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

echo ".env file created successfully!"

