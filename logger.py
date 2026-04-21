import os
import json
from datetime import datetime
from config import get_env

LOG_DIR = get_env('LOG_DIR', './logs')
LOG_FILE_PREFIX = get_env('LOG_FILE_PREFIX', 'sys_error')

os.makedirs(LOG_DIR, exist_ok=True)

def log_message(msg: dict) -> bool:
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    log_file = os.path.join(LOG_DIR, f"{LOG_FILE_PREFIX}_{date_str}.log")
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(msg, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        print(f"[Logger] Log file error: {e}")
        return False
