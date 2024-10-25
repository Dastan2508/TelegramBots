from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database


class FoodForm(StatesGroup):
    name_of_Food = State()
    price = State()
    from_countre = State()
    category = State()
    confirm = State()


admin =  5289719087
admin_Food_router = Router()
admin_Food_router.message.filter(F.from_user.id == admin)

@admin_Food_router.message(Command("newFood"))
async def start_Food_form(message: types.Message, state: FSMContext):
    await state.set_state(FoodForm.name_of_Food)
    await message.answer("Как называется ваше блюдо или напиток:")


@admin_Food_router.message(FoodForm.name_of_Food)
async def process_name_of_Food(message: types.Message, state: FSMContext):
    await state.update_data(name_of_Food=message.text)
    await state.set_state(FoodForm.price)
    await message.answer("Введите цену этого блюда или напитка:")


@admin_Food_router.message(FoodForm.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(FoodForm.from_countre)
    await message.answer("Из какой страны было создано это блюдо или напиток:")


@admin_Food_router.message(FoodForm.from_countre)
async def process_from_countre(message: types.Message, state: FSMContext):
    await state.update_data(from_countre=message.text)
    await state.set_state(FoodForm.category)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="Супы"),
            types.KeyboardButton(text="Вторые"),
            types.KeyboardButton(text="Горячие напитки"),
            types.KeyboardButton(text="Холодные напитки"),
            types.KeyboardButton(text="Гарниры")
        ]],
        resize_keyboard=True
    )
    await message.answer("Выберите категорию этого блюда или напитка:", reply_markup=kb)


@admin_Food_router.message(FoodForm.category)
async def proces_s_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]],
        resize_keyboard=True
    )
    await state.set_state(FoodForm.confirm)
    await message.answer(f"Название блюда: {data['name_of_Food']}\nЦена: {data['price']}\n"
                         f"В какой стране был создано: {data['from_countre']}\nКатегория: {data['category']}",
                         reply_markup=kb)


@admin_Food_router.message(FoodForm.confirm, F.text == "Да")
async def process_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    database.execute(
        query=("""
            INSERT INTO dishes (name_of_Food, price, from_countre, category)
            VALUES (?, ?, ?, ?)
        """),
        params=(
            data['name_of_Food'],
            data['price'],
            data['from_countre'],
            data['category'],
        )
    )

    await state.clear()
    await message.answer("Данные были сохранены!")


@admin_Food_router.message(FoodForm.confirm, F.text == "Нет")
async def process_not_confirmed(message: types.Message, state: FSMContext):
    await state.set_state(FoodForm.name_of_Food)
    await message.answer("Как называется ваше блюдо или напиток:")