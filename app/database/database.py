from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declared_attr, declarative_base

from app.database.utils import get_db_url, camel_to_snake


class ClsBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    def as_dict(self, *exclude_fields: str):
        """Возвращает данные в виде словаря"""
        exclude_fields = list(exclude_fields)
        exclude_fields.append("_sa_instance_state")
        return {
            name: value
            for name, value in self.__dict__.items()
            if name not in exclude_fields
        }


class Database:
    def __init__(self):
        self.engine = create_async_engine(
            get_db_url(),
            echo=False,
        )
        self.Base = declarative_base(cls=ClsBase)

        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    async def get_db(self) -> AsyncSession:
        """Функция для работы с базой данных."""
        try:
            async with self.SessionLocal() as db:
                yield db
        except SQLAlchemyError:
            await db.rollback()


database = Database()
Base = database.Base
SessionLocal = database.SessionLocal
