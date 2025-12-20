import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

if not PAYMENT_PROVIDER_TOKEN:
    raise ValueError("PAYMENT_PROVIDER_TOKEN не найден")
