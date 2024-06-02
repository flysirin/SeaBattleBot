import pickle
from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import default_state, State
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select, update, insert
from states.user_states import FSMUser
from models.database import async_session
from config_data.config_bot import bot_obj, bot_storage_key
from models.models import User
from services.SeaBattle import Game

storage = MemoryStorage()


async def register_user(user_id: int, username: str) -> None:
    user_storage_key = StorageKey(bot_id=bot_obj.id, user_id=user_id, chat_id=user_id)
    async with (async_session() as session):
        user_exists = await session.execute(select(User.user_id).where(User.user_id == user_id))
        if not user_exists.scalar():
            await session.execute(insert(User).values(username=username, user_id=user_id, size_field=10))
            await session.commit()
            await storage.set_data(bot=bot_obj, key=user_storage_key,
                                   data={'username': username, 'user_id': user_id,
                                         'in_game': False, 'size_field': 10,
                                         'user_game_field': None,
                                         'bot_game_field': None,
                                         })
            await session.close()


async def add_user_to_cur_session(user_id: int, username: str) -> None:
    cur_session_ids = await get_user_ids_from_cur_session()
    user_storage_key = StorageKey(bot_id=bot_obj.id, user_id=user_id, chat_id=user_id)

    if user_id not in cur_session_ids:
        cur_session_ids.add(user_id)
        await storage.update_data(bot=bot_obj, key=bot_storage_key, data={"cur_session_ids": cur_session_ids})

        async with (async_session() as session):
            is_game_query = await session.execute(select(User.in_game).where(User.user_id == user_id))
            is_game = is_game_query.scalar()
            if is_game:
                data = await session.execute(select(User.size_field,
                                                    User.user_game_field,
                                                    User.bot_game_field)
                                             .filter(User.user_id == user_id))
                for size_field, user_game_field, bot_game_field in data:
                    user_game_obj: object = pickle.loads(user_game_field)
                    bot_game_obj: object = pickle.loads(bot_game_field)

                    await storage.update_data(bot=bot_obj, key=user_storage_key,
                                              data={'username': username, 'user_id': user_id,
                                                    'in_game': is_game, 'size_field': size_field,
                                                    'user_game_field': user_game_obj,
                                                    'bot_game_field': bot_game_obj,
                                                    })


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
