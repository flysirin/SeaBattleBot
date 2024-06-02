from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config_bot import bot_obj
from models.methods import add_user_to_cur_session
from states.user_states import FSMUser
from aiogram.fsm.context import FSMContext


class UserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        await add_user_to_cur_session(user_id=message.from_user.id, username=message.from_user.username)
        return True





