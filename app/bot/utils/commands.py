from aiogram.types import BotCommand

# Список дефолтных команд
default_commands = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="tariff", description="Тарифы"),
    BotCommand(command="mysub", description="Мои подписки"),
    BotCommand(command="help", description="Задать вопрос"),
]
