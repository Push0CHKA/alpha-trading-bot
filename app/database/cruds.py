from datetime import timedelta, datetime

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.database.database import SessionLocal
from app.schemas.common_schemas import OrderStatus
from app.schemas.db_schema import Tariffs, Orders, UserTariff


async def get_tariffs():
    """Возвращает список тарифов"""
    try:
        async with SessionLocal() as db:
            tariffs = await db.execute(select(Tariffs))
            tariffs = tariffs.scalars().all()
    except SQLAlchemyError:
        await db.rollback()
        tariffs = None
    return tariffs


async def get_tariff(tariff_id: int) -> Tariffs:
    """Возвращает тарифа"""
    try:
        async with SessionLocal() as db:
            tariff = await db.execute(
                select(Tariffs).where(Tariffs.tariff_id == tariff_id)
            )
            tariff = tariff.scalars().one()
    except SQLAlchemyError:
        await db.rollback()
        raise
    return tariff


async def get_order(user_id: int, tariff_id: int) -> Orders:
    """Возвращает неоплаченный ордер, если существует"""
    try:
        async with SessionLocal() as db:
            order = await db.execute(
                select(Orders).where(
                    and_(
                        Orders.tariff_id == tariff_id,
                        Orders.user_id == user_id,
                        Orders.payment_status == OrderStatus.check.value,
                        Orders.created_date - datetime.now()
                        < timedelta(minutes=55),
                    )
                )
            )
            order = order.scalars().one()
    except NoResultFound:
        await db.rollback()
        order = None
    except SQLAlchemyError:
        await db.rollback()
        raise
    return order


async def add_order(order: Orders):
    """Добавление ордера в бд"""
    try:
        async with SessionLocal() as db:
            db.add(order)
            await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise


async def add_user_tariff(user_id: int, tariff_id: int):
    """Добавление связи user_id-tariff_id"""
    try:
        async with SessionLocal() as db:
            db.add(UserTariff(user_id=user_id, tariff_id=tariff_id))
            await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise
