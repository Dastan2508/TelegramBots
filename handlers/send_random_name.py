from aiogram import Router, types
from aiogram.filters.command import  Command
import random

random_router = Router()

names_list = ['Dastan', 'Emir', 'Adina', 'Asema', 'Kairat']

@random_router.message(Command("random"))
async def send_random_name(message: types.Message):
    random_name = random.choice(names_list)
    await message.reply(f"Список имен: {names_list}\n"
                        f"Случайное имя: {random_name}")

