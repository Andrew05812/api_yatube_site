@echo off
chcp 65001 >nul
echo ========================================
echo Запуск Django Backend сервера
echo ========================================
echo.

cd /d "%~dp0"

echo Активация виртуального окружения...
call env\Scripts\activate.bat

echo.
echo Проверка миграций...
python manage.py migrate --noinput

echo.
echo Запуск Django сервера на http://127.0.0.1:8000
echo Для остановки нажмите Ctrl+C
echo.
python manage.py runserver

pause

