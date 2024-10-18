import asyncio
import logging

from bot_config import bot, dp
from handlers.start import start_router
from handlers.info import info_router
from handlers.send_random_name import random_router
from handlers.review_dialog import opros_router


async def main():
    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(random_router)
    dp.include_router(opros_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
