from aiogram.dispatcher.filters.state import State, StatesGroup


class geo_choice(StatesGroup):
    location= State()