from enum import Enum


class UserLevel(str, Enum):
    """Уровень пользователя в системе"""

    admin = "admin"
    free = "free"
    friend = "friend"


class UserStatus(str, Enum):
    """Статус пользователя в системе"""

    active = "active"
    inactive = "inactive"


class OrderStatus(str, Enum):
    """Статус ордера"""

    check = "check"
    pay = "pay"
    paid_over = "paid_over"
    cancel = "cancel"


class PaymentAction(str, Enum):
    choose = "choose"
    check = "check"


# Список успешных статусов ордеров
SUCCESS_ORDER_STATUSES = [OrderStatus.pay.value, OrderStatus.paid_over.value]
