from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import default_state, State
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select, update, insert
from config_data.config import BOT_TOKEN, CUR_SESSION_ID
from states.user_states import FSMUser
from models.database import async_session
from config_data.config_bot import bot_obj, bot_storage_key
from models.models import User
from services.SeaBattle import Game

storage = MemoryStorage()


async def register_user(user_id: int, username: str) -> None:
    storage_key = StorageKey(bot_id=bot_obj.id, user_id=user_id, chat_id=user_id)
    await storage.set_data(bot=bot_obj, key=storage_key, data={'username': username, 'user_id': user_id,
                                                               'in_game': False, 'size_field': 10,
                                                               'user_game_field': None, 'bot_game_field': None,
                                                               })
    async with (async_session() as session):
        user_exists = await session.execute(select(User.user_id).where(User.user_id == user_id))
        if not user_exists.scalar():
            await session.execute(insert(User)
                                  .values(username=username, user_id=user_id, size_field=10))
            await session.commit()
        await session.close()


async def add_user_to_cur_session(user_id: int) -> None:
    cur_session_ids = await get_user_ids_from_cur_session()
    if user_id not in cur_session_ids:
        cur_session_ids.add(user_id)
        await storage.update_data(bot=bot_obj, key=bot_storage_key, data={"cur_session_ids": cur_session_ids})


async def get_user_ids_from_cur_session() -> set[int]:
    data = await storage.get_data(bot=bot_obj, key=bot_storage_key)
    cur_session_ids: set[int] = data.get("cur_session_ids", set())
    return cur_session_ids


async def init_game_session(user_state: FSMContext) -> None:
    size_field: int = (await user_state.get_data()).get('size_field', 10)
    user_game_field_obj = Game(size_field)
    bot_game_field_obj = Game(size_field)
    user_game_field_obj.init()
    bot_game_field_obj.init()

    await user_state.update_data(in_game=True, user_game_field=user_game_field_obj,
                                 bot_game_field=bot_game_field_obj)
