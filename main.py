import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers import commands
from config.config import config
from config.database import setup_scheduler, initialize_db


async def main():
    await initialize_db()
    
    bot = Bot(token=config.bot_token.get_secret_value())
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    dp = Dispatcher()

    # dp.include_routers(questions.router, different_types.router)
    dp.include_router(commands.router)

    # Настраиваем планировщик
    scheduler = await setup_scheduler(bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())