import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import user_handlers  # , other_handlers
from keyboards.set_menu import set_main_menu
from config_data.config import BOT_TOKEN
from models.database import init_models
from models.methods import on_startup, on_shutdown

logger = logging.getLogger(__name__)




async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=None)
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting bot")

    await init_models()


    dp = Dispatcher(storage=MemoryStorage())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(user_handlers.user_router)
    # dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
