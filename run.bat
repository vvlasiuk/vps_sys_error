@echo off
REM Активація venv та запуск сервісу
if not exist venv\Scripts\activate.bat (
    echo Віртуальне середовище не знайдено. Запустіть setup.bat
    exit /b 1
)
call venv\Scripts\activate.bat
python main.py
