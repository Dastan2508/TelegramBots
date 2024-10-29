from aiogram import Router, types, F
from aiogram.filters import Command
from bot_config import database

start_router = Router()
list_tg_ids = []


@start_router.message(Command(commands=['start']))
async def start_handler(message: types.Message):
    name = message.from_user.first_name

    unique_user_ids = database.fetch("SELECT DISTINCT user_id FROM users_id")
    summ = len(unique_user_ids)

    await message.answer(f"Вы уже {summ} зарегистрированный в боте")

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg"),
                types.InlineKeyboardButton(text="Наш инстаграм", url="https://www.instagram.com/adriano_restobar/")
            ],
            [
                types.InlineKeyboardButton(text="О нас", callback_data="about_us")
            ],
            [
                types.InlineKeyboardButton(text="Наш адрес",
                                           url="https://www.google.com/search?q=%D0%B0%D0%B4%D1%80%D0%B8%D0%B0%D0%BD%D0%BE")
            ],
            [
                types.InlineKeyboardButton(text="Вакансии", callback_data="vacancies")
            ],
            [
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="opros")
            ]
        ]
    )

    await message.answer(
        f"Добро пожаловать, {name}, в бот Noma! Этот бот был создан для вашего удобства. "
        f"Вы можете узнать о нашем ресторане, оставить отзыв, а также ознакомиться с нашими вакансиями.",
        reply_markup=keyboard
    )





