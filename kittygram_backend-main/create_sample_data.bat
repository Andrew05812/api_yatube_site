@echo off
chcp 65001 >nul
echo ========================================
echo Создание тестовых данных (котиков)
echo ========================================
echo.

cd /d "%~dp0"

echo Активация виртуального окружения...
call env\Scripts\activate.bat

echo.
echo Создание тестовых котиков...
python manage.py create_sample_data

echo.
echo ========================================
echo Готово! Тестовые данные созданы.
echo Пользователь: demo_user / demo123
echo ========================================
echo.
pause

