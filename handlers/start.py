from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

start_router = Router()

class Opros(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

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
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://noma.dk"),
                InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://www.instagram.com/noma")
            ],
            [
                InlineKeyboardButton(
                    text="Наши вакансии",
                    url="https://noma.dk/job/unsolicited-application-2/"),
                InlineKeyboardButton(
                    text="Наши контакты",
                    url="https://noma.dk/contact/")
            ],
            [
                InlineKeyboardButton(
                    text="Отзывы",
                    url="https://www.tripadvisor.com.au/Restaurant_Review-g189541-d694921-Reviews-Noma-Copenhagen_Zealand.html"),
                InlineKeyboardButton(
                    text="Наш адрес",
                    callback_data="location")
            ],
            [
                InlineKeyboardButton(
                    text="Бронировать столик",
                    callback_data="bron")
            ],
            [
                InlineKeyboardButton(
                    text="Оставить отзыв",
                    callback_data="leave_review")
            ]
        ]
    )
    await message.reply(
        f"Здравствуйте {name}!\n\n"
        "Добро пожаловать в*Noma! Мы рады приветствовать вас в нашем уникальном гастрономическом пространстве, "
        "где каждый элемент был создан с любовью и вниманием к деталям.\n\n"
        "Наша команда шеф-поваров, вдохновленная местными и сезонными продуктами, "
        "стремится предложить вам незабываемое кулинарное путешествие, сочетающее в себе традиции и современные техники.\n\n"
        "Мы надеемся, что ваш визит станет настоящим праздником для ваших вкусовых рецепторов!",
        reply_markup=kb
    )

@start_router.callback_query(F.data == "location")
async def loc_handler(callback: types.CallbackQuery):
    text = "Refshalevej 96, 1432 Копенгаген, Дания."
    await callback.answer(text)

@start_router.callback_query(F.data == "bron")
async def bron_handler(callback: types.CallbackQuery):
    text = "Вы забронировали столик"
    await callback.answer(text)

@start_router.callback_query(F.data == "leave_review")
async def review_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Как вас зовут?")
    await state.set_state(Opros.name)
    await callback.answer()

@start_router.message(Opros.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Ваш номер телефона или Инстаграм?")
    await state.set_state(Opros.phone_or_instagram)

@start_router.message(Opros.phone_or_instagram)
async def process_phone_or_instagram(message: types.Message, state: FSMContext):
    await state.update_data(phone_or_instagram=message.text)
    await message.answer("Дата вашего посещения нашего заведения?")
    await state.set_state(Opros.visit_date)

@start_router.message(Opros.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("1", "2", "3", "4", "5")
    await message.answer("Оцените качество еды (1 - плохо, 5 - отлично):", reply_markup=kb)
    await state.set_state(Opros.food_rating)




@start_router.message(Opros.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    user_data = await state.get_data()
    review_text = (
        f"Спасибо за ваш отзыв!\n\n"
        f"Имя: {user_data['name']}\n"
        f"Контакты: {user_data['phone_or_instagram']}\n"
        f"Дата посещения: {user_data['visit_date']}\n"
        f"Оценка еды: {user_data['food_rating']}\n"
        f"Оценка чистоты: {user_data['cleanliness_rating']}\n"
        f"Дополнительные комментарии: {user_data['extra_comments']}"
    )
    await message.answer(review_text)
    await state.clear()
