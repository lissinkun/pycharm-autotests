"""Настройки API: переменные окружения или значения по умолчанию."""

import os

BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))
