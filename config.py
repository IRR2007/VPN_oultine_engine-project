from outline_vpn.outline_vpn import OutlineVPN
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import logging
import os

# for outline-api
api_url = config("API_URL")
cert_sha256 = config("CERT_SHA")

DB_NAME: str = config("DB_NAME")
DB_DIR: str = config("DB_DIR")
DB_PORT: int = config("DB_PORT")

def database_url() -> str:
	os.makedirs(DB_DIR, exist_ok=True)
	return f"sqlite+aiosqlite:///{DB_DIR}/{DB_NAME}"

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

engine = create_async_engine(database_url(),
							 echo=True,
							 pool_size=10,
							 max_overflow=20
							 )
session_maker = async_sessionmaker(engine, expire_on_commit=False)

logger = set_logger()