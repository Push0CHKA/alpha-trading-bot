from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.config import buttons


# стартовая клавиатура
START_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons.TARIFFS),
            KeyboardButton(text=buttons.MY_SUBSCRIPTIONS),
        ],
        [
            # KeyboardButton(text=buttons.MY_ACCOUNT),
            KeyboardButton(text=buttons.HELP),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder=buttons.MAIN_INPUT_TEXT,
)
