import asyncio
from datetime import date

from aiogram import Bot
from config import db, logging

CHECK_INTERVAL = 24 * 60 * 60


async def check_and_notify(bot: Bot, today: date):
    keys = await db.get_all_keys()

    for key in keys:
        if not key.expiration_date:
            continue

        days_left = (key.expiration_date - today).days

        if days_left in (3, 1):
            await bot.send_message(
                chat_id=int(key.user),
                text=(
                    "⏰ *Подписка скоро закончится!*\n\n"
                    f"До окончания осталось *{days_left} "
                    f"{'день' if days_left == 1 else 'дня'}*.\n\n"
                    "Вы можете продлить подписку в разделе «💰 Тарифы»."
                ),
                parse_mode="Markdown"
            )


async def notify_expiring_subscriptions(bot: Bot):
    while True:
        try:
            logging.info("Running subscription expiration notifications check")
            await check_and_notify(bot, date.today())
            logging.info("Subscription notification check finished")
        except Exception as e:
            logging.error(f"Error in notification task: {e}")

        await asyncio.sleep(CHECK_INTERVAL)
