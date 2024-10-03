import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import dotenv_values
import logging
import random

token = dotenv_values('.env')['BOT_TOKEN']
bot = Bot(token=token)
dp = Dispatcher()

def load_users():
    try:
        with open('users.txt', 'r') as f:
            users = set(map(int, f.read().splitlines()))
    except FileNotFoundError:
        users = set()
    return users

def save_users(users):
    with open('users.txt', 'w') as f:
        f.write('\n'.join(map(str, users)))

def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.add(user_id)
        save_users(users)

def count_users():
    users = load_users()
    return len(users)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    add_user(user_id)
    unique_users_count = count_users()
    await message.answer(f"Привет, {name}!\n"
                         f"У нас {unique_users_count} уникальных пользователей.")

@dp.message(Command("info"))
async def send_info(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    await message.answer(f"id: {user_id}\n"
                         f"name: {first_name}\n"
                         f"user: {username}")

names_list = ['Dastan', 'Emir', 'Adina', 'Asema', 'Kairat']

@dp.message(Command("random"))
async def send_random_name(message: types.Message):
    random_name = random.choice(names_list)
    await message.reply(f"Список имен: {names_list}\n"
                        f"Случайное имя: {random_name}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
