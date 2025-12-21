from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.handlerDB import DataBaseHandler

DATABASE_URL = "sqlite+aiosqlite:///telegram_bot.db"

engine = create_async_engine(DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

db = DataBaseHandler(Session, engine)
