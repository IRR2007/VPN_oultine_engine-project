import asyncio

def bytes_to_gb(data):
	return data / 1024 / 1024 / 1024

class OutlineCommands():
	def __init__(self, client):
		self.client = client

	async def generate_new_key(self, username):
		try:
			key = await asyncio.to_thread(client.create_key)
			await asyncio.to_thread(client.rename_key, key.key_id, username)
			return key
		except Exception as e:
			print(f"Error while generating: {e}")
			return None

	async def delete_key(self, key):
		if key is not None:
			try:
				await asyncio.to_thread(client.delete_key, key.key_id)
				print(f"Deleted key {key.name}")
			except Exception as e:
				print(f"Error while deleting key {key.name}: {e}")

	async def get_keys_info(self):
		try:
			keys = await asyncio.to_thread(client.get_keys)
			for key in keys:
				print(f"NAME: {key.name}")
				print(f"ID: {key.key_id}")
				print(f"URL: {key.access_url}")
				try:
					print(f"DATA USED: {bytes_to_gb(int(key.used_bytes))} GB")
				except:
					print(f"DATA USED: {key.used_bytes}")
				print()
		except Exception as e:
			print(f"Error while getting information: {e}")
