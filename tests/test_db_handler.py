import pytest
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_add_key_and_get_user(db_handler):
    await db_handler.add_key(
        key_str="key1",
        user_name="alice",
        expiration=date.today() + timedelta(days=1),
        key_id=1,
    )

    user = await db_handler.get_key_user("key1")

    assert user == "alice"

@pytest.mark.asyncio
async def test_get_all_user_keys(db_handler):
    await db_handler.add_key(
        key_str="key1",
        user_name="bob",
        expiration=date.today(),
        key_id="1",
    )
    await db_handler.add_key(
        key_str="key2",
        user_name="bob",
        expiration=date.today(),
        key_id="2",
    )

    keys = await db_handler.get_all_user_keys("bob")

    assert set(keys) == {"key1", "key2"}

@pytest.mark.asyncio
async def test_delete_key(db_handler):
    await db_handler.add_key(
        key_str="delete_me",
        user_name="alice",
        expiration=date.today(),
        key_id=1,
    )

    await db_handler.delete_key("delete_me")

    user = await db_handler.get_key_user("delete_me")
    assert user is None

@pytest.mark.asyncio
async def test_update_expiration(db_handler):
    await db_handler.add_key(
        key_str="update_key",
        user_name="alice",
        expiration=date.today(),
        key_id="1",
    )

    new_date = date.today() + timedelta(days=10)
    updated = await db_handler.update_key_expiration_date(
        "update_key",
        new_date,
    )

    expiration = await db_handler.get_key_expiration_date("update_key")

    assert updated is True
    assert expiration == new_date

@pytest.mark.asyncio
async def test_valid_check_key(db_handler):
    await db_handler.add_key(
        key_str="expired",
        user_name="john",
        expiration=date.today() - timedelta(days=1),
        key_id="1",
    )

    is_valid = await db_handler.valid_check_key("expired")

    assert is_valid is False
