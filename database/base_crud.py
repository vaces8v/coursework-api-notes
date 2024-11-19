from sqlalchemy import select, insert, update, delete

from database.database import async_session_maker


class BaseCRUD:
    """Базовый класс, поддерживающий CRUD операции"""
    model = None

    # Чтение
    @classmethod
    async def find_all(cls, **filters):
        """Поиск всех записей по фильтру"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filters):
        """Поиск одной записи по фильтру"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        """Поиск одной записи по id"""
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Запись
    @classmethod
    async def create(cls, **data):
        """Создание записи"""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def create_and_return_id(cls, **data):
        """Создание и возврат id созданной записи"""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def create_and_return_all(cls, **data):
        """Создание и возврат созданной записи"""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalars().all()

    # Обновление
    @classmethod
    async def update(cls, model_id: int, **data):
        """Обновление записи по id"""
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(**data)
            await session.execute(query)
            await session.commit()

    # Удаление
    @classmethod
    async def delete(cls, model_id: int):
        """Удаление записи по id"""
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            await session.execute(query)
            await session.commit()