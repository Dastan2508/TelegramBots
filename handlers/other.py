from aiogram import types, Router
from aiogram.filters import Command

other = Router()
@other.message()
async def echo_handler(message):
    text = message.text
    await message.answer(text)