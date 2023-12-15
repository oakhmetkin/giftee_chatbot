from aiogram.dispatcher.filters.state import State, StatesGroup


class GiftRecState(StatesGroup):
    start = State()
    base_quest = State()
    deep_quest = State()
    lifestyle_quest = State()
    gift_desc = State()
    budget = State()
    check = State()
