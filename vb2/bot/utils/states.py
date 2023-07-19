from aiogram.dispatcher.filters.state import State, StatesGroup


class GetMark(StatesGroup):
    subject = State()
    mark = State()


class ChooseSpec(StatesGroup):
    search = State()
    words = State()