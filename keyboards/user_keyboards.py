from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


# from lexicon.lexicon import HOST_BUTTONS


def test_inline_kb(**kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for i in range(10):
            buttons.append(InlineKeyboardButton(text=f"{i}",
                                                callback_data=f"__{i}__player__user_id__"))

    kb_builder.row(*buttons)
    return kb_builder.as_markup()
