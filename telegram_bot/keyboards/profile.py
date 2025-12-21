from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🔄 Продлить подписку",
                callback_data="renew_sub"
            )]
        ]
    )