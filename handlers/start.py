from aiogram import Router, F, types
from aiogram.filters.command import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://geeks.kg"
                ),
                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://instagram.com/geekskg"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="О нас",
                    callback_data="aboutus"
                ),
                types.InlineKeyboardButton(
                    text="Оставить отзыв",
                    callback_data="opros"
                )
            ]
        ]
    )
    await message.reply(
        f"Привет, {name}. Добро пожаловать в наш бот для книголюбов",
        reply_markup=kb
    )

@start_router.callback_query(F.data == "opros")
async def review_handler(callback: types.CallbackQuery):
    await callback.message.answer("Нажмите на кнопу внизу чтобы продолжить:")
    await callback.message.answer("/opros")