from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router
from telegram_bot.keyboards.main_menu import main_menu_keyboard


router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! \n\n"
        "Выбери пункт меню",
        reply_markup=main_menu_keyboard()
    )