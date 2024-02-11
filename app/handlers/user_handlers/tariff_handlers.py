from datetime import timedelta

from aiogram import types, Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from app.config import buttons as btn, common_messages
from app.database.cruds import get_tariff, add_user_tariff
from app.handlers.user_handlers.common_handlers import tariff_cmd
from app.handlers.user_handlers.utils.callbacks import (
    PaymentCallback,
    PaymentAction,
)
from app.handlers.user_handlers.utils.payment import CryptoPayment
from app.keyboards.common_inline import (
    create_payment_inline_kb,
    create_invite_inline_kb,
)
from app.schemas.common_schemas import SUCCESS_ORDER_STATUSES

tariffs_router = Router(name=__name__)


@tariffs_router.message(F.text == btn.TARIFFS)
async def tariffs_button(message: types.Message):
    """Обработчик кнопки 'тарифы'"""
    await tariff_cmd(message)


@tariffs_router.callback_query(
    PaymentCallback.filter(F.action == PaymentAction.choose)
)
async def tariff_payment_callback(
    query: CallbackQuery,
    callback_data: PaymentCallback,
):
    """Обработчик кнопки выбора тарифа"""
    tariff = await get_tariff(tariff_id=int(callback_data.payment))
    await query.message.answer(
        text=common_messages.PAYMENT_MESSAGE.format(
            name=tariff.name,
            period=tariff.period,
            price=tariff.price,
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=await create_payment_inline_kb(
            user_id=int(query.from_user.id),
            tariff_id=int(callback_data.payment),
        ),
    )


@tariffs_router.callback_query(
    PaymentCallback.filter(F.action == PaymentAction.check)
)
async def check_tariff_payment_callback(
    query: CallbackQuery,
    callback_data: PaymentCallback,
    bot: Bot,
):
    """Проверка оплаты подписки"""
    response = await CryptoPayment().check_payment(
        payment_id=callback_data.payment
    )
    # счет оплачен
    if response.get("payment_status") in SUCCESS_ORDER_STATUSES:
        await add_user_tariff(
            user_id=int(query.from_user.id),
            tariff_id=int(callback_data.tariff),
        )
        tariff = await get_tariff(tariff_id=callback_data.tariff)
        chat_invite_links = list()
        # создание пригласительных ссылок
        for chat_id in tariff.canals:
            chat_invite_links.append(
                await bot.create_chat_invite_link(
                    chat_id=chat_id,
                    member_limit=1,
                    expire_date=timedelta(days=3),
                )
            )
        await query.message.answer(
            text=common_messages.SUCCESS_PAYMENT_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=await create_invite_inline_kb(chat_invite_links),
        )
    else:  # счет не оплачен
        await query.answer(
            text=common_messages.CHECK_PAYMENT_MESSAGE, cache_time=15
        )
