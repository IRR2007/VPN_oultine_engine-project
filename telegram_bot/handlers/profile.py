from aiogram import Router, F, types
from datetime import date

from config import db
from telegram_bot.keyboards.profile import profile_keyboard

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def profile_handler(message: types.Message):
    user_id = message.from_user.id
    today = date.today()

    # Получаем все ключи пользователя (у нас предполагается 1 ключ)
    user_keys = await db.get_all_user_keys(str(user_id))

    if not user_keys:
        await message.answer(
            "👤 *Мой профиль*\n\n"
            "🔒 Подписка: ❌ нет\n"
            "📅 Срок действия: —\n"
            "🔑 VPN-ключ: —",
            parse_mode="Markdown"
        )
        return

    access_url = user_keys[0]
    expiration = await db.get_key_expiration_date(access_url)

    if not expiration or expiration < today:
        status_text = "❌ неактивна"
        expires_text = "—"
    else:
        status_text = "✅ активна"
        expires_text = expiration.strftime("%d.%m.%Y")

    await message.answer(
        "👤 *Мой профиль*\n\n"
        f"🔒 Подписка: {status_text}\n"
        f"📅 Срок действия: {expires_text}\n"
        f"🔑 VPN-ключ:\n`{access_url}`",
        parse_mode="Markdown",
        reply_markup=profile_keyboard()
    )


@router.callback_query(F.data == "renew_sub")
async def renew_sub_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🔄 *Продление подписки*\n\n"
        "Выберите тариф для продления в разделе «💰 Тарифы».",
        parse_mode="Markdown"
    )
