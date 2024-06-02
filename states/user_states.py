from aiogram.filters.state import StatesGroup, State


class FSMUser(StatesGroup):
    # wait_start_game = State()
    game_process = State()
    # set_nickname = State()
