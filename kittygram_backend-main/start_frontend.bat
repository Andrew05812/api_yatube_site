@echo off
chcp 65001 >nul
echo ========================================
echo Запуск React Frontend сервера
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Проверка зависимостей...
if not exist "node_modules" (
    echo Установка зависимостей npm...
    call npm install
)

echo.
echo Запуск React dev server на http://localhost:3000
echo Для остановки нажмите Ctrl+C
echo.
call npm start

pause

