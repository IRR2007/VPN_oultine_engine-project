import pytest
from unittest.mock import AsyncMock

from telegram_bot.services.tasks import stop_expired_keys_once


@pytest.mark.asyncio
async def test_stop_expired_keys_once(mocker):
    mock_stop = AsyncMock()
    mocker.patch(
        "telegram_bot.services.tasks.outline.stop_expired_key",
        mock_stop
    )

    mocker.patch(
        "telegram_bot.services.tasks.db.get_all_invalid_keys_id",
        return_value=[1, 2, 3]
    )

    await stop_expired_keys_once()

    assert mock_stop.call_count == 3
