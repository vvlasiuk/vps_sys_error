import os
import json
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')
RESPONSIBILITY_PATH = os.path.join(BASE_DIR, 'config', 'responsibility.json')

load_dotenv(ENV_PATH)

def get_env(key, default=None):
    return os.getenv(key, default)

def load_responsibility():
    with open(RESPONSIBILITY_PATH, encoding='utf-8') as f:
        return json.load(f)
