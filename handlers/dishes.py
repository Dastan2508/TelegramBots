from aiogram import F, Router, types
from aiogram.filters import Command

from bot_config import database

catalog_router = Router()


@catalog_router.message(Command("catalog"))
async def show_all_dishes(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Супы"),
                types.KeyboardButton(text="Вторые"),
            ],
            [
                types.KeyboardButton(text="Горячие напитки"),
                types.KeyboardButton(text="Холодные напитки"),
                types.KeyboardButton(text="Гарниры")
            ]

        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите категорию"
    )
    await message.answer("Выберите категорию блюда", reply_markup=kb)

categoris = ("Супы", "Вторые", "Горячие напитки", "Холодные напитки", "Гарниры")


@catalog_router.message(F.text.in_(categoris))
async def show_dishes_by_category(message: types.Message):
    categori = message.text
    print(categori)
    dishes = database.fetch("SELECT * FROM dishes")
    print(dishes)
    await message.answer("Все наши блюда\n")
    for i in dishes:
        msg = f"Название: {i['name_of_Food']}\nЦена: {i['price']}"
        await message.answer(msg)