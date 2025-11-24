@echo off
chcp 65001 >nul
echo ========================================
echo Запуск Kittygram - Backend и Frontend
echo ========================================
echo.

cd /d "%~dp0"

echo Запуск Backend сервера в новом окне...
start "Kittygram Backend" cmd /k "%~dp0start_backend.bat"

timeout /t 3 /nobreak >nul

echo Запуск Frontend сервера в новом окне...
start "Kittygram Frontend" cmd /k "%~dp0start_frontend.bat"

echo.
echo ========================================
echo Оба сервера запущены!
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Откройте браузер и перейдите на http://localhost:3000
echo.
echo Для остановки закройте оба окна или нажмите Ctrl+C в каждом окне
echo ========================================
echo.
pause

