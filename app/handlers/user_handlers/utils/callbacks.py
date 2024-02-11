from aiogram.filters.callback_data import CallbackData

from app.schemas.common_schemas import PaymentAction


class PaymentCallback(CallbackData, prefix="payment"):
    action: PaymentAction
    payment: int | str
    tariff: int | None = None
