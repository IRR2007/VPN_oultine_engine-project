from outline_vpn.outline_vpn import OutlineVPN
from decouple import config
import logging

# for outline-api
api_url = config("API_URL")
cert_sha256 = config("CERT_SHA")
client = OutlineVPN(api_url = api_url, cert_sha256 = cert_sha256)

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

logger = set_logger()