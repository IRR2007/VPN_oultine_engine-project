from aiogram import Router, F, types
from telegram_bot.keyboards.tariffs import tariffs_keyboard, confirm_tariff_keyboard
from config import PAYMENT_PROVIDER_TOKEN
from telegram_bot.services.outline import outline

from database.db import db

from datetime import datetime, timedelta, timezone

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
    await callback.message.edit_text(
        "💰 Выберите тариф:",
        reply_markup=tariffs_keyboard()
    )


@router.callback_query(F.data.startswith("pay_"))
async def pay_handler(callback: types.CallbackQuery):
    await callback.answer()

    days = int(callback.data.split("_")[1])
    price = PRICES.get(days)

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

    user_keys = await db.get_all_user_keys(str(user_id))

    if user_keys:
        access_url = user_keys[0]
        old_expiration = await db.get_key_expiration_date(access_url)

        if old_expiration and old_expiration.tzinfo is None:
            old_expiration = old_expiration.replace(tzinfo=timezone.utc)

        if old_expiration and old_expiration > now:
            new_expiration = old_expiration + timedelta(days=days)
        else:
            new_expiration = now + timedelta(days=days)

        await db.update_key_expiration_date(access_url, new_expiration)

        await message.answer(
            "🔄 *Подписка успешно продлена!*\n\n"
            f"📦 Продление: {days} дней\n"
            f"📅 Новый срок: {new_expiration.strftime('%d.%m.%Y %H:%M')}\n\n"
            "🔑 VPN-ключ остаётся прежним.",
            parse_mode="Markdown"
        )

    else:
        key = await outline.generate_new_key(username)

        if not key or not key.access_url:
            await message.answer(
                "⚠️ Оплата прошла, но не удалось создать VPN-ключ.\n"
                "Пожалуйста, обратитесь в поддержку."
            )
            return

        expiration = now + timedelta(days=days)

        await db.add_key(
            key_str=key.access_url,
            user_name=str(user_id),
            expiration=expiration
        )

        await message.answer(
            "✅ *Оплата прошла успешно!*\n\n"
            f"📦 Тариф: {days} дней\n"
            f"📅 Действует до: {expiration.strftime('%d.%m.%Y %H:%M')}\n\n"
            f"🔑 *Ваш VPN-ключ:*\n`{key.access_url}`",
            parse_mode="Markdown"
        )
