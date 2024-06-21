from aiogram.fsm.state import State, StatesGroup

class GroupSelection(StatesGroup):
    waiting_group = State()
    waiting_time = State()