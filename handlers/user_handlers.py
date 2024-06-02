from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from filters.filters import UserFilter
from keyboards.user_keyboards import test_inline_kb
from lexicon.lexicon import USER_LEXICON, USER_BUTTONS
from states.user_states import FSMUser
from aiogram.filters import StateFilter, Text, CommandStart, Command
from aiogram.types import Message, CallbackQuery
# from lexicon.lexicon import LEXICON, BUTTONS
from keyboards.user_keyboards import user_keyboard
from models.methods import register_user, init_game_session
user_router = Router()


user_router.message.filter(UserFilter())
user_router.callback_query.filter(UserFilter())


@user_router.message(CommandStart(), StateFilter(default_state))
async def start_handler(message: Message, state: FSMContext):
    await register_user(user_id=message.from_user.id, username=message.from_user.username)
    await message.answer(USER_LEXICON['/start'],
                         reply_markup=user_keyboard())


@user_router.message(Command(commands=['help']))
async def help_handler(message: Message, state: FSMContext):
    await message.answer(USER_LEXICON['/help'])


@user_router.message(Text(USER_BUTTONS['new_game']))
async def start_game_handler(message: Message, state: FSMContext):
    await state.set_state(FSMUser.game_process)
    await init_game_session(user_state=state)
    await message.delete()


@user_router.message(Text(USER_BUTTONS['end_game']), StateFilter(FSMUser.game_process))
async def start_game_handler(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.delete()


@user_router.message(Text(USER_BUTTONS['settings']), StateFilter(default_state))
async def start_game_handler(message: Message, state: FSMContext):
    # await state.set_data()
    await message.delete()


@user_router.message()
async def delete_message(message: Message, state: FSMContext):
    await message.delete()