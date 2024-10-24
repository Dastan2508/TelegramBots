import asyncio
import logging

from bot_config import bot, dp
from handlers.start import start_router
from handlers.info import info_router
from handlers.send_random_name import random_router
from handlers.review_dialog import opros_router
from handlers.add_food import admin_Food_router
from handlers.other import other
from handlers.dishes import catalog_router
from bot_config import bot, dp, database
from aiogram import Bot


async def on_startup():
    print("База данных созданнна")
    database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(random_router)
    dp.include_router(opros_router)

    dp.include_router(admin_Food_router)
    dp.include_router(catalog_router)

    dp.include_router(other)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())