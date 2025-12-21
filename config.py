from outline_vpn.outline_vpn import OutlineVPN
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import logging
import os
from dotenv import load_dotenv

#for tg-bot
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

if not PAYMENT_PROVIDER_TOKEN:
    raise ValueError("PAYMENT_PROVIDER_TOKEN не найден")


# for outline-api
api_url = config("API_URL")
cert_sha256 = config("CERT_SHA")

# database
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")

def database_url() -> str:
    return (
        f"postgresql+asyncpg://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# for logging
def set_logger():
	logging.basicConfig(
		level = logging.INFO,
		format = "%(asctime)s - %(levelname)s - %(message)s",
		handlers = [
			logging.FileHandler("log.log"),
			logging.StreamHandler()
		]
	)
	return logging.getLogger(__name__)


client = OutlineVPN(api_url = api_url, cert_sha256 = cert_sha256)

engine = create_async_engine(database_url())
session_maker = async_sessionmaker(engine, expire_on_commit=False)

logger = set_logger()