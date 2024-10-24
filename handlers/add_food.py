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