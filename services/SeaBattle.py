from random import randint, choice


class Ship:
    def __init__(self, length, tp: [1, 0] = 1, x=None, y=None, cells: list = None, size_field=10):
        self._x, self._y = x, y
        self._tp = tp
        self._length = length  # number of decks
        self._is_move = True
        self.cells_state = cells if cells else [1 for _ in range(length)]  # condition of ship: 1 or 2 - damage
        self.ship_cells, self._around_ship = set(), set()
        self._size_field = size_field
        if type(x) is int and type(y) is int:
            self.cells_ship_id()
            self.cells_around_ship_id()

    def set_start_coords(self, x, y):
        self._x, self._y = x, y
        self.cells_ship_id()
        self.cells_around_ship_id()

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go: int):  # move ship, example: -1 or 1
        if any(x == 2 for x in self.cells_state):
            self._is_move = False
            return False
        self._x = self._x + go * self._tp
        self._y = self._y + go * (self._tp ^ 1)
        self.cells_ship_id()
        self.cells_around_ship_id()
        return True

    def cells_ship_id(self):  # set cells ship id
        self.ship_cells = {(self._y + i * (self._tp ^ 1)) * self._size_field + self._x + i * self._tp + 1 for i in
                           range(self._length)}

    def cells_around_ship_id(self):  # set cells surrounding the ship id
        self._around_ship = set()
        for shift in range(self._length):
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if 0 <= self._x + shift * self._tp + i < self._size_field and 0 <= self._y + shift * (
                            self._tp ^ 1) + j < self._size_field:
                        self._around_ship.add((self._y + shift * (self._tp ^ 1) + j) * self._size_field + (
                                self._x + shift * self._tp + i) + 1)

    def is_collide(self, ship: 'Ship'):  # -> True, if there is a collision with another ship
        if self.ship_cells and self._around_ship and ship._around_ship and ship.ship_cells:
            return not self._around_ship.isdisjoint(ship.ship_cells)

    def is_out_pole(self, size):  # -> True, if there is going beyond borders
        size = self._size_field if not size else size
        for shift in range(self._length):
            if not (0 <= self._x + shift * self._tp < size and 0 <= self._y + shift * (self._tp ^ 1) < size):
                return True
        return False

    def __getitem__(self, index):  # get condition ship cell
        return self.cells_state[index]

    def __setitem__(self, index, value):  # set condition ship cell
        if value != 2:
            raise ValueError("Expected type int = 2")
        self.cells_state[index] = value
        self._is_move = False

    def __repr__(self):
        return f"s{self._length, self._x, self._y},tp={self._tp}"


class Game:
    def __init__(self, size=10, ships: list[Ship] = None):
        self._size = size
        self._c_size = size - 1  # coordinates size
        self._ships = ships if ships else []
        self._field = [[0 for _ in range(size)] for _ in range(size)]
        self._miss_field = [[0 for _ in range(size)] for _ in range(size)]

    def size(self):
        return self._size

    def init(self):
        def lineup_ships():
            ships_start_init = []
            for length in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
                ships_start_init.append(Ship(length=length, tp=randint(0, 1), size_field=self._size))

            [ship.set_start_coords(x=randint(0, self._c_size), y=randint(0, self._c_size)) for ship in ships_start_init]
            self._ships = []
            count = 0
            for ship in ships_start_init:
                if not self._ships:
                    while ship.is_out_pole(self._size):
                        ship.set_start_coords(x=randint(0, self._c_size), y=randint(0, self._c_size))
                    self._ships.append(ship)
                else:
                    while any(end_ship.is_collide(ship) or ship.is_out_pole(self._size) for end_ship in self._ships):
                        count += 1
                        if count > 300:
                            return
                        ship.set_start_coords(x=randint(0, self._c_size), y=randint(0, self._c_size))
                    self._ships.append(ship)

        while len(self._ships) != 10:
            lineup_ships()
        self._upd_field()

    def _upd_field(self):
        self._field = [[0 for _ in range(self._size)] for _ in range(self._size)]
        for ship in self._ships:
            x_0, y_0 = ship.get_start_coords()
            turn, not_turn = (ship._tp ^ 1), ship._tp
            c = 0
            for cell_ship in ship:
                self._field[y_0 + c * turn][x_0 + c * not_turn] = cell_ship
                c += 1

    def get_field_with_ships(self):
        return tuple(tuple(x) for x in self._field)

    def get_miss_field(self):
        return tuple(tuple(x) for x in self._miss_field)

    def _can_move(self, ship: Ship, distance: int):
        if not ship._is_move:
            return False
        last_ships = [l_ship for l_ship in self._ships if l_ship != ship]
        go_ship = Ship(ship._length, ship._tp, ship._x, ship._y, size_field=self._size)
        go_ship.move(distance)
        for another_ship in last_ships:
            if go_ship.is_out_pole(self._size) or another_ship.is_collide(go_ship):
                return False
        return True

    def move_ships(self):  # move ships to -1 or 1 cell
        for ship in self._ships:
            go_trip = choice((-1, 1))
            if self._can_move(ship, go_trip):
                ship.move(go_trip)
            elif self._can_move(ship, -go_trip):
                ship.move(-go_trip)
        self._upd_field()

    def _get_ship_by_cell_id(self, cell_id: int):
        if self._ships:
            for ship in self._ships:
                if cell_id in ship.ship_cells:
                    return ship

    def damage_register(self, x: int, y: int):
        """x,y ∈ [1-field_size]. 1 - for ship, 2 - for damage, 3 - for miss"""
        if not (1 <= x <= self._size and 1 <= y <= self._size):
            return
        cell_id = (y - 1) * self._size + x
        ship = self._get_ship_by_cell_id(cell_id)
        if ship:
            ship._is_move = False
            num_cell_id = sorted(ship.ship_cells).index(cell_id)
            ship.cells_state[num_cell_id] = 2
            self._upd_field()
        else:
            self._miss_field[y - 1][x - 1] = 3

    def get_field_for_owner(self):
        res_field = [[0 for _ in range(self._size)] for _ in range(self._size)]
        for y in range(self._size):
            for x in range(self._size):
                if self._field[y][x] in (1, 2):
                    res_field[y][x] = self._field[y][x]
                else:
                    res_field[y][x] = self._miss_field[y][x]
        return res_field

    def get_field_for_enemy(self):
        res_field = [[0 for _ in range(self._size)] for _ in range(self._size)]
        for y in range(self._size):
            for x in range(self._size):
                if self._field[y][x] == 2:
                    res_field[y][x] = 2
                else:
                    res_field[y][x] = self._miss_field[y][x]
        return res_field


# pole = Game(10)
# pole.init()
# print(pole.get_ships())
# pole.show()
# pole.move_ships()
# print()
# pole.show()
# print()
# print(pole.get_ships())
