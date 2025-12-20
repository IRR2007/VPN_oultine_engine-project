from aiogram import Router, F, types
from  telegram_bot.keyboards.tariffs import tariffs_keyboard, confirm_tariff_keyboard
from telegram_bot.config import PAYMENT_PROVIDER_TOKEN
from telegram_bot.services.outline import outline

from datetime import datetime, timedelta, timezone

USER_SUBSCRIPTIONS = {}

router = Router()
PRICES = {7: 99, 14: 179, 30: 299}

@router.message(F.text == "💰 Тарифы")
async def tariffs_handler(message: types.Message):
    await message.answer(
        "💰 Выберите тариф",
        reply_markup=tariffs_keyboard()
    )


@router.callback_query(F.data.startswith("tariff_"))
async def tariff_choice_handler(callback: types.CallbackQuery):
    await callback.answer()

    days = int(callback.data.split("_")[1])
    price = PRICES.get(days)

    if price is None:
        await callback.message.edit_text("❌ Неизвестный тариф")
        return

    await callback.message.edit_text(
        f"✅ Вы выбрали тариф на {days} дней — {price} ₽\n\n"
        f"Нажмите «Оплатить», чтобы продолжить",
        reply_markup=confirm_tariff_keyboard(days)
    )


@router.callback_query(F.data == "back_to_tariffs")
async def back_to_tariffs_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("💰 Выберите тариф:", reply_markup=tariffs_keyboard())


@router.callback_query(F.data.startswith("pay_"))
async def pay_handler(callback: types.CallbackQuery):
    await callback.answer()

    days = int(callback.data.split("_")[1])
    price = PRICES.get(days)

    # await callback.message.answer(
    #     f"💳 Оплата за {days} дней ({price} ₽) пока не подключена\n"
    # )
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"VPN подписка на {days} дней",
        description=f"Тестовая оплата подписки на {days} дней",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            types.LabeledPrice(
                label=f"{days} дней",
                amount=price * 100
            )
        ],
        payload=f"vpn_{days}_days"
    )


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)



@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    payment = message.successful_payment

    payload = payment.invoice_payload
    days = int(payload.split("_")[1])

    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    now = datetime.now(timezone.utc)

    existing = USER_SUBSCRIPTIONS.get(user_id)
    existing_vpn = existing.get("vpn") if existing else None

    if existing and existing["subscription"]["expires_at"] > now:
        expires_at = existing["subscription"]["expires_at"] + timedelta(days=days)
    else:
        expires_at = now + timedelta(days=days)

    paid_at = now

    if existing_vpn and existing_vpn.get("access_url"):
        key = None
    else:
        key = await outline.generate_new_key(username)

    # сохраняем в память
    USER_SUBSCRIPTIONS[user_id] = {
        "user": {
            "telegram_id": user_id,
            "username": message.from_user.username,
            "full_name": message.from_user.full_name,
        },
        "subscription": {
            "days": days,
            "paid_at": paid_at,
            "expires_at": expires_at,
            "is_active": True,
        },
        "payment": {
            "payload": payload,
            "amount": payment.total_amount,
            "currency": payment.currency,
        },
        "vpn": existing_vpn if existing_vpn else {
            "access_url": key.access_url if key else None,
            "key_id": key.key_id if key else None,
        },
    }

    if key:
        # новый ключ
        await message.answer(
            "✅ *Оплата прошла успешно!*\n\n"
            f"📦 Тариф: {days} дней\n"
            f"📅 Действует до: {expires_at.strftime('%d.%m.%Y %H:%M')}\n\n"
            f"🔑 *Ваш VPN-ключ:*\n`{key.access_url}`",
            parse_mode="Markdown"
        )

    elif existing_vpn and existing_vpn.get("access_url"):
        # продление
        await message.answer(
            "🔄 *Подписка успешно продлена!*\n\n"
            f"📦 Продление: {days} дней\n"
            f"📅 Новый срок: {expires_at.strftime('%d.%m.%Y %H:%M')}\n\n"
            "🔑 VPN-ключ остаётся прежним.",
            parse_mode="Markdown"
        )

    else:
        # реальная ошибка
        await message.answer(
            "⚠️ Оплата прошла, но не удалось создать VPN-ключ.\n"
            "Пожалуйста, обратитесь в поддержку."
        )
