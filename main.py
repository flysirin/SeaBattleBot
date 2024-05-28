import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import user_handlers  # , other_handlers
from keyboards.set_menu import set_main_menu
from config_data.config import BOT_TOKEN
from models.database import get_db, init_db
# from models.models import User


logger = logging.getLogger(__name__)


# async def on_startup(dispatcher: Dispatcher):
#     session = next(get_db())
#     users_data = await session.query(User).all()




async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting bot")
    bot = Bot(token=BOT_TOKEN, parse_mode=None)
    dp = Dispatcher()

    dp.include_router(user_handlers.user_router)
    # dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
