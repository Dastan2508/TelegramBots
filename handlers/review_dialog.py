from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

opros_router = Router()

class Opros(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()



@opros_router.message(F.text == 'стоп')
async def stop_opros_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос остановлен!")

@opros_router.message(Command('opros'))  # Запуск опроса по команде /opros
async def start_opros_handler(message: types.Message, state: FSMContext):
    await state.set_state(Opros.name)
    await message.answer("Как Вас зовут?")

@opros_router.message(Opros.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Opros.phone_number)
    await message.answer("Ваш номер телефона или Instagram:")

@opros_router.message(Opros.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(Opros.visit_date)
    await message.answer("Дата вашего посещения нашего заведения:")

@opros_router.message(Opros.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(Opros.food_rating)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Как оцениваете качество еды?", reply_markup=kb)

@opros_router.message(Opros.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(Opros.cleanliness_rating)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Как оцениваете чистоту заведения?", reply_markup=kb)

@opros_router.message(Opros.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(Opros.extra_comments)
    await message.answer("Дополнительные комментарии/жалоба:")

@opros_router.message(Opros.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()
    await message.answer(f"Спасибо за отзыв, {data['name']}! Вот что вы указали:\n"
                         f"Номер телефона/Instagram: {data['phone_number']}\n"
                         f"Дата посещения: {data['visit_date']}\n"
                         f"Оценка еды: {data['food_rating']}\n"
                         f"Оценка чистоты: {data['cleanliness_rating']}\n"
                         f"Комментарии: {data['extra_comments']}")

    await state.clear()