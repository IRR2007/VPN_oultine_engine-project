import asyncio
from config import logging
from typing import Any, List

def bytes_to_gb(data) -> int:
	return data / 1024 / 1024 / 1024

class OutlineCommands():
	def __init__(self, client) -> None:
		self.client = client

	async def generate_new_key(self, username):
		try:
			key = await asyncio.to_thread(self.client.create_key)
			await asyncio.to_thread(self.client.rename_key, key.key_id, username)
			return key
		except Exception as e:
			logging.info(f"Error while generating: {e}")
			return None

	async def delete_key(self, key) -> None:
		if key is not None:
			try:
				await asyncio.to_thread(self.client.delete_key, key.key_id)
				logging.info(f"Deleted key {key.name}")
			except Exception as e:
				logging.info(f"Error while deleting key {key.name}: {e}")

	async def get_keys_info(self) -> List[Any]:
		try:
			keys = await asyncio.to_thread(self.client.get_keys)
			for key in keys:
				print(f"NAME: {key.name}\nID: {key.key_id}\nURL: {key.access_url}")
				try:
					print(f"DATA USED: {bytes_to_gb(int(key.used_bytes))} GB\n")
				except:
					print(f"DATA USED: {key.used_bytes}\n")
			return keys
		except Exception as e:
			logging.info(f"Error while getting information: {e}")
