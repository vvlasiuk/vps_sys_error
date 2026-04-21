# VPS System Error Service

## Швидкий старт

1. Клонувати репозиторій:
   ```
git clone <repo_url>
cd vps_sys_error
```
2. Створити та активувати віртуальне середовище, встановити залежності:
   - Windows:
     ```
     setup.bat
     ```
   - Linux/macOS:
     ```
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
3. Заповнити `.env` (приклад у `.env`).
4. Запустити сервіс:
   ```
   python main.py
   ```

## Опис
Сервіс для обробки системних помилок, логування та маршрутизації у Telegram, Email, Slack через RabbitMQ.

## Структура
- `main.py` — точка входу
- `config.py` — завантаження конфігурацій
- `rabbitmq.py` — робота з RabbitMQ
- `logger.py` — логування
- `dispatcher.py` — маршрутизація
- `channels/` — канали доставки
- `config/responsibility.json` — конфіг каналів

## VS Code
Для автоматичного вибору venv додайте у `.vscode/settings.json`:
```
{
  "python.defaultInterpreterPath": "venv/Scripts/python.exe"
}
```
(або відповідний шлях для Linux/macOS)
