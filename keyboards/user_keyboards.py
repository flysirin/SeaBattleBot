from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import USER_BUTTONS


def user_keyboard() -> ReplyKeyboardMarkup:
    start_game = KeyboardButton(text=USER_BUTTONS['new_game'])
    end_game = KeyboardButton(text=USER_BUTTONS['end_game'])
    settings = KeyboardButton(text=USER_BUTTONS['settings'])
    keyboard = ReplyKeyboardMarkup(keyboard=[[start_game], [end_game], [settings]],
                                   one_time_keyboard=True,
                                   resize_keyboard=True)
    return keyboard


def test_inline_kb(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for i in range(10):
            buttons.append(InlineKeyboardButton(text=f"{i}",
                                                callback_data=f"__{i}__player__user_id__"))

    kb_builder.row(*buttons)
    return kb_builder.as_markup()
