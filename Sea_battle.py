from pprint import pprint


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._x, self._y = x, y
        self._tp = tp
        self._length = length  # number of decks
        self._is_move = True
        self._cells = [1 for _ in range(length)]          # condition of ship: 1 or 2
        self._turn, self._not_turn = tp - 1, not (tp - 1)   # 1 or 0  - turning the ship

    def set_start_coords(self, x, y):

        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go: int):                # move ship, example: -1 or 1
        if not self._is_move:
            print("Move isn't real, the ship is hit")
            return
        if Ship(self._length, self._tp, self._x + go * self._not_turn, self._y + go * self._turn).is_out_pole():
            print("Move isn't real, the ship will go beyond the borders")
            return
        self._x = self._x + go * self._not_turn
        self._y = self._y + go * self._turn

    @property
    def cells_ship_id(self):            # set cells ship id
        return {(self._y + i * self._turn) * SIZE_GAME_POLE + self._x + i * self._not_turn + 1 for i in range(self._length)}

    @property
    def cells_around_ship_id(self):       # set cells surrounding the ship id
        aura_ship = set()
        for shift in range(self._length):
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if 0 <= self._x + shift * self._not_turn + i < SIZE_GAME_POLE and 0 <= self._y + shift * self._turn + j < SIZE_GAME_POLE:
                        aura_ship.add((self._y + shift * self._turn + j) * SIZE_GAME_POLE + (self._x + shift * self._not_turn + i) + 1)
        return aura_ship

    def is_collide(self, ship: 'Ship'):   # -> True, if there is a collision
        return not self.cells_around_ship_id.isdisjoint(ship.cells_ship_id)

    def is_out_pole(self, size=10):       # -> True, if there is going beyond borders
        for shift in range(self._length):
            if not (0 <= self._x + shift * self._not_turn < size and 0 <= self._y + shift * self._turn < size):
                return True
        return False

    def __getitem__(self, index):   # get condition ship cell
        return self._cells[index]

    def __setitem__(self, index, value):  # set condition ship cell
        if value not in (1, 2):
            raise ValueError("Expected type int with: 1 or 2")
        self._cells[index] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []

    def size(self):
        return self._size


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
ship_1 = Ship(4, tp=2, x=1, y=1)
ship_2 = Ship(2, tp=2, x=3, y=2)
pprint(ship_1.cells_ship_id)
pprint(ship_1.cells_around_ship_id)
print(ship_1.is_out_pole())

print(ship_1.is_collide(ship_2))
