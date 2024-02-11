from datetime import timedelta, datetime

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from aiogram.types import Message

from app.database.database import SessionLocal
from app.schemas.common_schemas import OrderStatus
from app.schemas.db_schema import Tariffs, Orders, UserTariff, Users
from app.config import common_messages as com_msg


async def get_tariffs(tariff_ids: list = None) -> list[Tariffs] | None:
    """Возвращает список тарифов
    :param tariff_ids: Список с id выборки тарифов
    :return Tariffs: Тарифы
    """
    try:
        async with SessionLocal() as db:
            if not tariff_ids:
                tariffs = await db.execute(select(Tariffs))
            else:
                tariffs = await db.execute(
                    select(Tariffs).where(Tariffs.tariff_id.in_(tariff_ids))
                )
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
            tariff = await db.execute(
                select(Tariffs).where(Tariffs.tariff_id == tariff_id)
            )
            tariff = tariff.scalars().one()
            db.add(
                UserTariff(
                    user_id=user_id,
                    tariff_id=tariff_id,
                    finish_date=datetime.now() + timedelta(days=tariff.period),
                )
            )
            await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise


async def get_user_subscriptions(user_id: int) -> list[UserTariff]:
    """Возвращает активные подписки пользователя"""
    try:
        async with SessionLocal() as db:
            user_tariffs = await db.execute(
                select(UserTariff).where(
                    and_(
                        UserTariff.finish_date > datetime.now(),
                        UserTariff.user_id == user_id,
                    )
                )
            )
            user_tariffs = user_tariffs.scalars().all()
    except NoResultFound:
        await db.rollback()
        user_tariffs = []
    except SQLAlchemyError:
        await db.rollback()
        raise
    return user_tariffs


async def add_new_user(message: Message):
    """Добавление нового пользователя
    :param message: Объект сообщения телеграм
    """
    try:
        async with SessionLocal() as db:
            db.add(
                Users(
                    user_id=message.chat.id,
                    username=message.chat.username,
                    first_name=message.chat.first_name,
                    last_name=message.chat.last_name,
                )
            )
            await db.commit()
    except IntegrityError:
        # пользователь уже существует
        ...
    except SQLAlchemyError:
        await db.rollback()
        raise


async def user_active_subscriptions(user_id: int) -> str | None:
    """
    Возвращает строку с активными подписками
    :param user_id: ID пользователя
    """
    user_subs = await get_user_subscriptions(user_id)
    if not user_subs:
        return com_msg.NO_ACTIVE_SUBSCRIPTIONS
    else:
        tariffs = {
            tariff.tariff_id: tariff
            for tariff in await get_tariffs(
                [tariff.tariff_id for tariff in user_subs]
            )
        }
        user_subs_str = com_msg.ACTIVE_SUBS_TITTLE
        for user_sub in user_subs:
            user_subs_str += com_msg.ACTIVE_SUBS_STR.format(
                sub=tariffs[user_sub.tariff_id].name,
                date=user_sub.finish_date.strftime("%d\\.%m\\.%Y %H\\:%M"),
            )
        return user_subs_str
