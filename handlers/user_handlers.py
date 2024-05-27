from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from keyboards.user_keyboards import test_inline_kb
from lexicon.lexicon import USER_LEXICON
from states.user_states import FSMUser
from aiogram.filters import StateFilter, Text, CommandStart, Command
from aiogram.types import Message, CallbackQuery
# from lexicon.lexicon import LEXICON, BUTTONS
from keyboards import user_keyboards

user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer(USER_LEXICON['/start'])


@user_router.message(Command(commands=['help']))
async def help_handler(message: Message, state: FSMContext):
    await message.answer(USER_LEXICON['/help'])



