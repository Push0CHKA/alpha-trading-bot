from os import getenv
from asyncio import run as arun

from aiogram import Bot, Dispatcher, types

from app.bot.utils.commands import default_commands
from app.bot.utils.app_event_handlers import on_startup
from app.bot.utils.params import ALLOWED_UPDATES
from app.handlers.user_handlers.common_handlers import user_common_router
from app.handlers.user_handlers.help_handlers import help_user_router
from app.handlers.user_handlers.tariff_handlers import tariffs_router
from app.handlers.user_handlers.subscriptions_handlers import subs_router

bot = Bot(token=getenv("TOKEN"))

dp = Dispatcher()

dp.include_router(user_common_router)
dp.include_router(help_user_router)
dp.include_router(tariffs_router)
dp.include_router(subs_router)


async def run_bot():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=default_commands,
        scope=types.BotCommandScopeDefault(),
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


def run():
    arun(run_bot())
