from aiogram import types, Router, F

from app.config import buttons as btn
from app.handlers.user_handlers.common_handlers import my_subscription_cmd

subs_router = Router(name=__name__)


@subs_router.message(F.text == btn.MY_SUBSCRIPTIONS)
async def my_subscriptions_button(message: types.Message):
    """Обработчик кнопки 'мои подписки'"""
    await my_subscription_cmd(message)
