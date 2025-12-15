from database.models import Key, Base
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, update, delete
from typing import List, Optional


# import asyncio
# import os


class DataBaseHandler:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession], engine) -> None:
        self.session_maker = session_maker
        self.engine = engine

    async def create_db(self) -> None:
        """Создает базу данных"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self) -> None:
        """УНИЧТОЖАЮТ БАЗУ ДАННЫХ"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def add_key(self, key_str: str, user_name: str, expiration: datetime) -> None:
        """Добавляет ключ ОБРАТИТЕ ВНИМАНИЕ ЧТО ТРЕБУЕТСЯ UTC!!!"""
        async with self.session_maker() as session:
            new_key: Key = Key(access_url=key_str, user=user_name, expiration_date=expiration)
            session.add(new_key)
            await session.commit()

    async def delete_key(self, key_str: str) -> None:
        """Удаляет ключ"""
        async with self.session_maker() as session:
            result = await session.execute(select(Key).where(Key.access_url == key_str))
            key_obj = result.scalar_one_or_none()
            if key_obj:
                await session.delete(key_obj)
                await session.commit()

    async def get_all_keys(self):
        """Возвращает все ключи - скорее всего не понадобится"""
        async with self.session_maker() as session:
            query = select(Key)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_key_user(self, key_str: str) -> Optional[str]:
        """Возвращает юзернейм пользователя владеющим данным ключом"""
        async with self.session_maker() as session:
            query = select(Key).where(Key.access_url == key_str)
            result = await session.execute(query)
            return result.scalar()

    async def get_all_user_keys(self, user_name: str) -> List[str]:
        """Возвращает список всех ключей (НЕ ORM-объектов!),
          которые принадлежат пользователю с данным юзернеймом"""
        async with self.session_maker() as session:
            query = select(Key.access_url).where(Key.user == user_name)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_key_expiration_date(self, key_str: str) -> Optional[datetime]:
        """Возвращает "срок годности" ключа по самому ключу"""
        async with self.session_maker() as session:
            query = select(Key.expiration_date).where(Key.access_url == key_str)
            result = await session.execute(query)
            return result.scalar()

    async def valid_check_key(self, key_str: str) -> Optional[bool]:
        """Проверяет истек ли "срок годности" ключа"""
        expiration = await self.get_key_expiration_date(key_str)
        if expiration is None:
            return None
        return datetime.now(datetime.timezone.utc) <= expiration

    async def update_key_expiration_date(self, key_str: str, new_expiration: datetime) -> bool:
        """Обновляет срок годности ключа"""
        async with self.session_maker() as session:
            query = (
                update(Key)
                .where(Key.access_url == key_str)
                .values(expiration_date=new_expiration)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
