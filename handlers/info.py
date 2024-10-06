from aiogram import Router, types
from aiogram.filters.command import  Command

info_router = Router()


@info_router.message(Command("info"))
async def send_info(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    await message.answer(f"id: {user_id}\n"
                         f"name: {first_name}\n"
                         f"user: {username}")