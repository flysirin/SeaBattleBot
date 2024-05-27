import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import user_handlers  #, other_handlers
from keyboards.set_menu import set_main_menu
from config_data.config import BOT_TOKEN


# Logger initialise
logger = logging.getLogger(__name__)


# Function for configure and run Bot
async def main():
    # configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting bot")
    bot = Bot(token=BOT_TOKEN, parse_mode=None)
    dp = Dispatcher()

    # Register routers in Dispatcher
    dp.include_router(user_handlers.user_router)
    # dp.include_router(other_handlers.router)

    # Pass all updates and run polling
    await bot.delete_webhook(drop_pending_updates=True)

    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())





