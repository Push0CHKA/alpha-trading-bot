from app.database.database import database
from app.schemas.db_schema import Base


async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
