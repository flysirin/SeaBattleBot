from aiogram import Dispatcher, Bot
from aiogram.client import bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import default_state, State
from states.user_states import FSMUser
from models.database import get_db
from models.models import User

storage = MemoryStorage()


async def on_startup(dispatcher: Dispatcher):
    async with get_db() as session:
        users_data = await session.query(User).all()
        bot = Bot.get_current()
        for user in users_data:
            user_id = user.user_id
            storage_key = StorageKey(bot_id=bot.id, user_id=user_id, chat_id=user_id)
            await dispatcher.storage.set_data(bot=bot, key=storage_key,
                                              data={'user_id': user.user_id, 'username': user.username,
                                                    'size_field': user.size_field, 'in_game_field': user.in_game,
                                                    })
            state = FSMUser.game_process if user.in_game else default_state()
            await dispatcher.storage.set_state(bot=bot, key=storage_key, state=state)


async def on_shutdown(dispatcher: Dispatcher):
    async with get_db() as session:
        bot = Bot.get_current()
        user_data_db = await session.query(User).all()

        for user_data in user_data_db:
            storage_key = StorageKey(bot_id=bot.id, user_id=user_data, chat_id=user_data[0])
            print(user_data)
            user_data = await dispatcher.storage.get_data(bot=bot, key=storage_key)
            if user_data[1]:
                pass




