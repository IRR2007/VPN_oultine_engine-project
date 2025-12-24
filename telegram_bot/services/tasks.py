import asyncio
from config import db, client, logging
from outline_api.commands import OutlineCommands

outline = OutlineCommands(client)

CHECK_INTERVAL = 24 * 60 * 60


async def stop_expired_keys_task():
    while True:
        try:
            logging.info("Running expired keys check")

            invalid_keys = await db.get_all_invalid_keys_id()

            if invalid_keys:
                for key_id in invalid_keys:
                    await outline.stop_expired_key(key_id)

            logging.info("Expired keys check finished")

        except Exception as e:
            logging.error(f"Error in expired keys task: {e}")

        await asyncio.sleep(CHECK_INTERVAL)
