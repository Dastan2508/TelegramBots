from aiogram import Router, F, types
from aiogram.types import  Message, InlineKeyboardMarkup
from aiogram.filters.command import  Command

start_router = Router()

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

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    add_user(user_id)
    unique_users_count = count_users()
    await message.answer(f"У нас {unique_users_count} уникальных пользователей.")
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://noma.dk"),

                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://www.instagram.com/noma")
            ],
            [

                types.InlineKeyboardButton(
                    text="Наши вакансии",
                    url="https://noma.dk/job/unsolicited-application-2/"),

                types.InlineKeyboardButton(
                    text="Наши контакты",
                    url="https://noma.dk/contact/"

                )


            ],
            [
                types.InlineKeyboardButton(
                    text="Отзывы",
                    url="https://www.tripadvisor.com.au/Restaurant_Review-g189541-d694921-Reviews-Noma-Copenhagen_Zealand.html"),


                types.InlineKeyboardButton(
                    text="Наш адрес",
                    callback_data="location"

                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Бронировать столик",
                    callback_data="bron"

                )
            ]
        ]
    )
    await message.reply(
        f"Здравствуйте {name}!\n\n"
        "Добро пожаловать в Noma! Мы рады приветствовать вас в нашем уникальном гастрономическом пространстве, "
        "где каждый элемент был создан с любовью и вниманием к деталям.\n\n"
        "Наша команда шеф-поваров, вдохновленная местными и сезонными продуктами, "
        "стремится предложить вам незабываемое кулинарное путешествие, сочетающее в себе традиции и современные техники.\n\n"
        "Мы надеемся, что ваш визит станет настоящим праздником для ваших вкусовых рецепторов!",
        reply_markup=kb
    )


@start_router.callback_query(F.data == "location")
async def loc_handler(callback: types.CallbackQuery):
    text ="Refshalevej 96, 1432 Копенгаген, Дания."
    await callback.answer(text)

@start_router.callback_query(F.data == "bron")
async def bron_handler(callback: types.CallbackQuery):
    text ="Вы забронировали столик"
    await callback.answer(text)