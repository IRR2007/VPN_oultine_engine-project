# import asyncio
# from outline_api.commands import OutlineCommands
# from config import client, logging
#
# async def main():
# 	#код снизу можно спокойно убрать, это я для примера добавил.
# 	#кстати скажу заранее, запускать прогу для тесте лучше всего
# 	#через команду python3 -m telegram_bot.main в Python_Project.
# 	#Пытался делать относительные выводы, но он ругается, поэтому
# 	#пришлось так.
# 	print("/start")
# 	outline_class = OutlineCommands(client)
# 	await outline_class.get_keys_info()
#
# if __name__ == "__main__":
# 	asyncio.run(main())

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram import F
from telegram_bot.keyboards.main_menu import main_menu_keyboard
from  telegram_bot.keyboards.tariffs import tariffs_keyboard, confirm_tariff_keyboard
from telegram_bot.handlers.start import router as start_router
from telegram_bot.handlers.tariffs import router as tariffs_router
from telegram_bot.handlers.profile import router as profile_router
from telegram_bot.handlers.support import router as support_router

from telegram_bot.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(tariffs_router)
dp.include_router(profile_router)
dp.include_router(support_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
