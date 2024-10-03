import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import dotenv_values
import logging

import random

token = dotenv_values('.env')['BOT_TOKEN']
bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Привет, {name}!")

@dp.message(Command("info"))
async def send_info(message: types.Message):
    id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    await message.answer(f"id: {id}\n"
                         f"name: {first_name}\n"
                         f"user: {username}")


list = ['Dastan', 'Emir', 'Adina', 'Asema', 'Kairat']
@dp.message(Command("random"))
async def send_random_name(message: types.Message):
    random_name = random.choice(list)
    await message.reply(f"Список имен: {list}\n"
                        f"Случайное имя: {random_name}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())