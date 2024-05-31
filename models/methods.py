from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import default_state, State
from sqlalchemy import select, update
from config_data.config import BOT_TOKEN
from states.user_states import FSMUser
from models.database import async_session
from models.models import User
from services.SeaBattle import Game
import pickle

storage = MemoryStorage()


async def on_startup(dispatcher: Dispatcher):
    async with async_session() as session:
        chunked_iterator = await session.execute(select(User.user_id,
                                                        User.username,
                                                        User.in_game,
                                                        User.size_field))
    bot_obj = Bot(token=BOT_TOKEN, parse_mode=None)
    for user_data in chunked_iterator:
        user_id, username, in_game, size_field = user_data

        storage_key = StorageKey(bot_id=bot_obj.id, user_id=user_id, chat_id=user_id)
        await dispatcher.storage.set_data(bot=bot_obj, key=storage_key,
                                          data={'user_id': user_id, 'username': username,
                                                'size_field': size_field, 'in_game': in_game,
                                                })
        if in_game:
            result = await session.execute(select(User.user_game_field, User.bot_game_field)
                                              .where(User.user_id == user_id))
            user_game_byte, bot_game_byte = result.fetchone()
            # print(user_game_byte)
            # print(bot_game_byte)

        state = FSMUser.game_process if in_game else default_state
        await dispatcher.storage.set_state(bot=bot_obj, key=storage_key, state=state)
        await session.close()


async def on_shutdown(dispatcher: Dispatcher):
    async with async_session() as session:
        bot_obj = Bot(token=BOT_TOKEN, parse_mode=None)
        iter_user_ids = await session.execute(select(User.user_id))

        for user_data_id in iter_user_ids:
            user_id = user_data_id[0]
            storage_key = StorageKey(bot_id=bot_obj.id, user_id=user_id, chat_id=user_id)
            user_data = await dispatcher.storage.get_data(bot=bot_obj, key=storage_key)

            size_field = user_data.get('size_field', None)
            in_game = user_data.get('in_game', False)
            if not in_game:
                await session.execute(update(User)
                                      .where(User.user_id == user_id)
                                      .values(size_field=size_field, in_game=in_game))
            else:
                user_game_obj: Game = user_data.get('user_game_field', Game(size_field))
                bot_game_obj: Game = user_data.get('bot_game_field', Game(size_field))
                user_game_field: bytes = pickle.dumps(user_game_obj)
                bot_game_field: bytes = pickle.dumps(bot_game_obj)

                await session.execute(update(User)
                                      .where(User.user_id == user_id)
                                      .values(size_field=size_field, in_game=in_game,
                                              user_game_field=user_game_field,
                                              bot_game_field=bot_game_field))

        await session.commit()
        await session.close()

        print("END BOT! Close and commit!")
        # for user_data in user_data_db:
        #     print(user_data)
        #     user_data = await dispatcher.storage.get_data(bot=bot, key=storage_key)
        #     if user_data[1]:
        #         pass
