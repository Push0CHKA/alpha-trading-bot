from aiogram import types, Router, F

from app.config import buttons as btn
from app.handlers.user_handlers.common_handlers import help_cmd

help_user_router = Router(name=__name__)


@help_user_router.message(F.text == btn.HELP)
async def help_button(message: types.Message):
    """Обработчик кнопки 'поддержка'"""
    await help_cmd(message)
