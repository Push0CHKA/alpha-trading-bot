from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    func,
    Uuid,
    ARRAY,
)

from app.database.database import Base
from app.schemas.common_schemas import UserLevel, UserStatus, OrderStatus
from app.schemas.mixins import CreatedDateMixin


class Users(CreatedDateMixin, Base):
    """Таблица с пользователями"""

    user_id = Column(BigInteger, primary_key=True)
    nickname = Column(String, default=None)
    first_name = Column(String, default=None)
    last_name = Column(String, default=None)
    phone_number = Column(String, default=None)
    level = Column(String, nullable=False, default=UserLevel.free.value)
    status = Column(String, nullable=False, default=UserStatus.inactive.value)


class Tariffs(CreatedDateMixin, Base):
    """Таблица с тарифами"""

    tariff_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    period = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    canals = Column(ARRAY(BigInteger), nullable=False)


class UserTariff(Base):
    """Таблица пользователь-тариф"""

    user_id = Column(BigInteger, primary_key=True)
    tariff_id = Column(BigInteger, primary_key=True)
    buy_date = Column(
        DateTime,
        default=datetime.now,
        server_default=func.now(),
        primary_key=True,
    )


class Orders(CreatedDateMixin, Base):
    """Таблица с ордерами пользователей"""

    uuid = Column(String, primary_key=True)
    order_id = Column(Uuid, nullable=False)
    tariff_id = Column(Integer, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    url = Column(String, nullable=False)
    payment_status = Column(
        String, nullable=False, default=OrderStatus.check.value
    )
