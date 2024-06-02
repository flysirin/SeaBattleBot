from aiogram import Bot
from config_data.config import BOT_TOKEN
from aiogram.fsm.storage.base import StorageKey


bot_obj = Bot(token=BOT_TOKEN, parse_mode='HTML')
bot_storage_key = StorageKey(bot_id=bot_obj.id, user_id=bot_obj.id, chat_id=bot_obj.id)

