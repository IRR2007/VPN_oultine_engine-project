from unittest.mock import AsyncMock, MagicMock
from outline_api.commands import OutlineCommands, bytes_to_gb
import pytest
import asyncio

def test_bytes_to_gb():
    assert bytes_to_gb(1024**3) == 1
    assert bytes_to_gb(0) == 0
    assert bytes_to_gb(3 * 1024**3) == 3

@pytest.fixture
def mock_client():
    client = MagicMock()
    client.create_key = MagicMock(return_value = MagicMock(key_id = "67", name = "test_key", access_url = "url", used_bytes = 0))
    client.rename_key = MagicMock()
    client.add_data_limit = MagicMock()
    client.delete_key = MagicMock()
    client.get_keys = MagicMock(return_value = [MagicMock(key_id = "67", name = "test_key", access_url = "url", used_bytes = 1024**3)])
    return client

@pytest.fixture
def outline_commands(mock_client):
    return OutlineCommands(mock_client)

@pytest.mark.asyncio
async def test_generate_new_key(outline_commands, mock_client):
    username = "user1"
    key = await outline_commands.generate_new_key(username)
    assert key.key_id == "67"
    mock_client.rename_key.assert_called_once_with("67", username)
    mock_client.add_data_limit.assert_called_once_with("67", 3 * 10**12)

@pytest.mark.asyncio
async def test_delete_key(outline_commands, mock_client):
    key = MagicMock(key_id = "67", name = "test_key")
    await outline_commands.delete_key(key)
    mock_client.delete_key.assert_called_once_with("67")

@pytest.mark.asyncio
async def test_stop_expired_key(outline_commands, mock_client):
    await outline_commands.stop_expired_key("67")
    mock_client.add_data_limit.assert_called_with("67", 0)

@pytest.mark.asyncio
async def test_start_expired_key(outline_commands, mock_client):
    await outline_commands.start_expired_key("67")
    mock_client.add_data_limit.assert_called_with("67", 3 * 10**12)
