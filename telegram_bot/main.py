import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram import F
from telegram_bot.keyboards.main_menu import main_menu_keyboard
from telegram_bot.keyboards.tariffs import tariffs_keyboard, confirm_tariff_keyboard
from telegram_bot.handlers.start import router as start_router
from telegram_bot.handlers.tariffs import router as tariffs_router
from telegram_bot.handlers.profile import router as profile_router
from telegram_bot.handlers.support import router as support_router
from telegram_bot.services.tasks import stop_expired_keys_task

from config import BOT_TOKEN

from config import db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(tariffs_router)
dp.include_router(profile_router)
dp.include_router(support_router)


async def main():
    await db.create_db()

    asyncio.create_task(stop_expired_keys_task())

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
