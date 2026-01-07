from aiogram.fsm.state import StatesGroup, State


class DemoStates(StatesGroup):
    start = State()
    dashboard = State()
    activation = State()
    trust_info = State()
    scenario = State()
