from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile

from app.database.cruds import add_new_user, user_active_subscriptions
from app.keyboards.common_inline import create_tariffs_inline_kb
from app.config import common_messages as com_msg
from app.keyboards import common_keyboards as ckb

user_common_router = Router(name=__name__)


@user_common_router.message(CommandStart())
async def start_cmd(message: types.Message):
    """Обработчик команды 'старт'"""
    await add_new_user(message)
    await message.answer_photo(
        photo=FSInputFile(path="./files/welcome.png"),
        caption=com_msg.WELCOME_MESSAGE,
        reply_markup=ckb.START_KEYBOARD,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@user_common_router.message(Command("help"))
async def help_cmd(message: types.Message):
    """Обработчик команды 'помощь'"""
    await message.answer(
        com_msg.HELP_MESSAGE,
        reply_markup=ckb.START_KEYBOARD,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@user_common_router.message(Command("tariff"))
async def tariff_cmd(message: types.Message):
    """Обработчик команды 'тарифы'"""
    await message.delete()
    await message.answer(
        com_msg.TARIFFS_MESSAGE,
        reply_markup=await create_tariffs_inline_kb(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@user_common_router.message(Command("mysub"))
async def my_subscription_cmd(message: types.Message):
    """Обработчик команды 'мои подписки'"""
    await message.answer(
        await user_active_subscriptions(message.from_user.id),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
