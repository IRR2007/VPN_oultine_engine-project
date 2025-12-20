from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💰 Тарифы"),
                KeyboardButton(text="👤 Мой профиль"),
            ],
            [
                KeyboardButton(text="🆘 Поддержка"),
                KeyboardButton(text="📖 Инструкция"),
            ],
        ],
        resize_keyboard=True
    )