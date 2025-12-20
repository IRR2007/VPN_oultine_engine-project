from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def tariffs_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="7 дней - 99 ₽", callback_data="tariff_7")],
            [InlineKeyboardButton(text="14 дней - 179 ₽", callback_data="tariff_14")],
            [InlineKeyboardButton(text="30 дней - 299 ₽", callback_data="tariff_30")],
        ]
    )


def confirm_tariff_keyboard(days: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", callback_data=f"pay_{days}")],
            [InlineKeyboardButton(text="⬅️ Назад к тарифам", callback_data="back_to_tariffs")],
        ]
    )
