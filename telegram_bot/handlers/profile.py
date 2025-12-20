from aiogram import Router, F, types
from telegram_bot.handlers.tariffs import USER_SUBSCRIPTIONS
from telegram_bot.keyboards.profile import profile_keyboard

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def profile_handler(message: types.Message):
    user_id = message.from_user.id
    data = USER_SUBSCRIPTIONS.get(user_id)

    if not data:
        await message.answer(
            "👤 *Мой профиль*\n\n"
            "🔒 Подписка: ❌ нет\n"
            "📅 Срок действия: —\n"
            "🔑 VPN-ключ: —",
            parse_mode="Markdown"
        )
        return

    subscription = data["subscription"]
    vpn = data.get("vpn")

    expires_at = subscription["expires_at"].strftime("%d.%m.%Y %H:%M")
    vpn_text = vpn["access_url"] if vpn and vpn.get("access_url") else "—"

    await message.answer(
        "👤 *Мой профиль*\n\n"
        "🔒 Подписка: ✅ активна\n"
        f"📅 Срок действия: {expires_at}\n"
        f"🔑 VPN-ключ:\n`{vpn_text}`",
        parse_mode="Markdown",
        reply_markup=profile_keyboard()
    )


@router.callback_query(F.data == "renew_sub")
async def renew_sub_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🔄 Продление подписки\n\n"
        "Выберите тариф для продления в разделе «💰 Тарифы»."
    )