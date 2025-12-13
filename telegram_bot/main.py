import asyncio
from outline_api.commands import OutlineCommands
from config import client, logging

async def main():
	#код снизу можно спокойно убрать, это я для примера добавил.
	#кстати скажу заранее, запускать прогу для тесте лучше всего
	#через команду python3 -m telegram_bot.main в Python_Project.
	#Пытался делать относительные выводы, но он ругается, поэтому
	#пришлось так.
	print("/start")
	outline_class = OutlineCommands(client)
	await outline_class.get_keys_info()

if __name__ == "__main__":
	asyncio.run(main())