import pytest
from datetime import date, timedelta
from unittest.mock import AsyncMock

from telegram_bot.services.notifications import check_and_notify


class FakeKey:
    def __init__(self, user, expiration_date):
        self.user = user
        self.expiration_date = expiration_date


@pytest.mark.asyncio
async def test_notify_when_3_days_left(mocker):
    fake_bot = AsyncMock()
    today = date.today()

    fake_keys = [
        FakeKey(user="123", expiration_date=today + timedelta(days=3))
    ]

    mocker.patch(
        "telegram_bot.services.notifications.db.get_all_keys",
        return_value=fake_keys
    )

    await check_and_notify(fake_bot, today)

    fake_bot.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_no_notify_when_more_than_3_days(mocker):
    fake_bot = AsyncMock()
    today = date.today()

    fake_keys = [
        FakeKey(user="123", expiration_date=today + timedelta(days=10))
    ]

    mocker.patch(
        "telegram_bot.services.notifications.db.get_all_keys",
        return_value=fake_keys
    )

    await check_and_notify(fake_bot, today)

    fake_bot.send_message.assert_not_called()
