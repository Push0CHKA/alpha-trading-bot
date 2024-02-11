from aiogram.types import InlineKeyboardMarkup, ChatInviteLink
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from app.config import inline_buttons
from app.database.cruds import get_tariffs, get_tariff, get_order, add_order
from app.handlers.user_handlers.utils.callbacks import (
    PaymentCallback,
    PaymentAction,
)
from app.handlers.user_handlers.utils.payment import CryptoPayment
from app.schemas.db_schema import Orders


async def create_tariffs_inline_kb() -> InlineKeyboardMarkup:
    """Создание inline-клавиатуры с тарифами"""
    # список тарифов
    tariffs = await get_tariffs()
    kb_inline = InlineKeyboardBuilder()
    for tariff in tariffs:
        kb_inline.row(
            InlineKeyboardButton(
                text=inline_buttons.TARIFF_INLINE_BTN.format(
                    name=tariff.name,
                    period=tariff.period,
                    price=tariff.price,
                ),
                callback_data=PaymentCallback(
                    action=PaymentAction.choose,
                    payment=tariff.tariff_id,
                ).pack(),
            )
        )
    # TODO сделать обработчик отсутствия тарифов
    return kb_inline.as_markup()


async def create_payment_inline_kb(
    user_id: int, tariff_id: int
) -> InlineKeyboardMarkup:
    """Inline-клавиатура для оплаты тарифа"""
    # тариф для оплаты
    tariff = await get_tariff(tariff_id=tariff_id)
    # проверка на существование неоплаченного ордера
    order = await get_order(user_id=user_id, tariff_id=tariff_id)
    if order:
        # ссылка для оплаты
        payment_url = order.url
        # id ордера (нужен для проверки)
        payment_id = order.uuid
    else:
        # делаем запрос для получения данных оплаты
        payment_request = await CryptoPayment.make_payment(price=tariff.price)
        # ссылка для оплаты
        payment_url = payment_request.get("url")
        # id ордера (нужен для проверки)
        payment_id = payment_request.get("uuid")
        await add_order(
            order=Orders(
                uuid=payment_id,
                order_id=payment_request.get("order_id"),
                tariff_id=tariff_id,
                user_id=user_id,
                url=payment_url,
            )
        )
    kb_inline = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(
                    text=inline_buttons.PAYMENT_INLINE_BTN, url=payment_url
                )
            ],
            [
                InlineKeyboardButton(
                    text=inline_buttons.CHECK_PAYMENT_INLINE_BTN,
                    callback_data=PaymentCallback(
                        action=PaymentAction.check,
                        payment=payment_id,
                        tariff=tariff_id,
                    ).pack(),
                )
            ],
        ]
    )
    return kb_inline.as_markup()


async def create_invite_inline_kb(
    invite_links: list[ChatInviteLink],
) -> InlineKeyboardMarkup:
    """Создание inline-клавиатуры с приглашениями"""
    kb_inline = InlineKeyboardBuilder()
    for index, invite in enumerate(invite_links):
        kb_inline.row(
            InlineKeyboardButton(
                text=inline_buttons.INVITE_INLINE_BTN.format(index=index + 1),
                url=invite.invite_link,
            )
        )
    return kb_inline.as_markup()
