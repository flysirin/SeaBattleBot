from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import default_state, State
from sqlalchemy import select, update
from config_data.config import BOT_TOKEN, CUR_SESSION_ID
from states.user_states import FSMUser
from models.database import async_session
from models.models import User
from services.SeaBattle import Game
import pickle

# storage = MemoryStorage()


async def on_startup(dispatcher: Dispatcher):
    bot_obj = Bot(token=BOT_TOKEN, parse_mode=None)
    storage_key = StorageKey(bot_id=bot_obj.id, user_id=bot_obj.id, chat_id=bot_obj.id)
    await dispatcher.storage.set_data(bot=bot_obj, key=storage_key, data={"cur_session_ids": set()})


async def on_shutdown(dispatcher: Dispatcher):
    bot_obj = Bot(token=BOT_TOKEN, parse_mode=None)
    storage_key = StorageKey(bot_id=bot_obj.id, user_id=bot_obj.id, chat_id=bot_obj.id)
    data = await dispatcher.storage.get_data(bot=bot_obj, key=storage_key)
    current_session_ids: set[int] = data.get("cur_session_ids", set())

    for user_id in current_session_ids:
        storage_key = StorageKey(bot_id=bot_obj.id, user_id=user_id, chat_id=user_id)
        user_data = await dispatcher.storage.get_data(bot=bot_obj, key=storage_key)

        async with async_session() as session:
            in_game = user_data.get('in_game', False)
            size_field = user_data.get('size_field', 10)
            if in_game:
                user_game_obj: Game = user_data.get('user_game_field', Game(size_field))
                bot_game_obj: Game = user_data.get('bot_game_field', Game(size_field))
                user_game_field: bytes = pickle.dumps(user_game_obj)
                bot_game_field: bytes = pickle.dumps(bot_game_obj)

                await session.execute(update(User)
                                      .where(User.user_id == user_id)
                                      .values(size_field=size_field, in_game=in_game,
                                              user_game_field=user_game_field,
                                              bot_game_field=bot_game_field))
            else:
                await session.execute(update(User)
                                      .where(User.user_id == user_id)
                                      .values(size_field=size_field, in_game=in_game))

            await session.commit()
            await session.close()
            print("END BOT! Close and commit!")
