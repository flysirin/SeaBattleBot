from random import randint, choice


class Ship:
    def __init__(self, length, tp=1, x=None, y=None, size=10):
        self._x, self._y = x, y
        self._tp = tp
        self._length = length  # number of decks
        self._is_move = True
        self._cells = [1 for _ in range(length)]  # condition of ship: 1 or 2
        self._turn, self._not_turn = tp - 1, not (tp - 1)  # 1 or 0  - turning the ship
        self._ship_cells, self._around_ship = set(), set()
        self._size = size
        if type(x) == int and type(y) == int and type(size) == int:
            self.cells_ship_id()
            self.cells_around_ship_id()

    def set_start_coords(self, x, y):
        self._x, self._y = x, y
        self.cells_ship_id()
        self.cells_around_ship_id()

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go: int):  # move ship, example: -1 or 1
        if any(x == 2 for x in self._cells):
            self._is_move = False
            return False
        self._x = self._x + go * self._not_turn
        self._y = self._y + go * self._turn
        self.cells_ship_id()
        self.cells_around_ship_id()
        return True

    def cells_ship_id(self):  # set cells ship id
        self._ship_cells = {(self._y + i * self._turn) * self._size + self._x + i * self._not_turn + 1 for i in
                            range(self._length)}

    def cells_around_ship_id(self):  # set cells surrounding the ship id
        self._around_ship = set()
        for shift in range(self._length):
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if 0 <= self._x + shift * self._not_turn + i < self._size and 0 <= self._y + shift * self._turn + j < self._size:
                        self._around_ship.add((self._y + shift * self._turn + j) * self._size + (
                                self._x + shift * self._not_turn + i) + 1)

    def is_collide(self, ship: 'Ship'):  # -> True, if there is a collision with another ship
        if self._ship_cells and self._around_ship and ship._around_ship and ship._ship_cells:
            return not self._around_ship.isdisjoint(ship._ship_cells)

    def is_out_pole(self, size):  # -> True, if there is going beyond borders
        size = self._size if not size else size
        for shift in range(self._length):
            if not (0 <= self._x + shift * self._not_turn < size and 0 <= self._y + shift * self._turn < size):
                return True
        return False

    def __getitem__(self, index):  # get condition ship cell
        return self._cells[index]

    def __setitem__(self, index, value):  # set condition ship cell
        if value != 2:
            raise ValueError("Expected type int = 2")
        self._cells[index] = value
        self._is_move = False

    def __repr__(self):
        return f"s{self._length, self._x, self._y},tp={self._tp}"


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._c_size = size - 1  # coordinates size
        self._ships = []
        self._pole = [[0 for _ in range(size)] for _ in range(size)]

    def size(self):
        return self._size

    def init(self):
        def lineup_ships():
            ships_start_init = [Ship(4, tp=randint(1, 2), size=self._size), Ship(3, tp=randint(1, 2), size=self._size),
                                Ship(3, tp=randint(1, 2), size=self._size), Ship(2, tp=randint(1, 2), size=self._size),
                                Ship(2, tp=randint(1, 2), size=self._size), Ship(2, tp=randint(1, 2), size=self._size),
                                Ship(1, tp=randint(1, 2), size=self._size), Ship(1, tp=randint(1, 2), size=self._size),
                                Ship(1, tp=randint(1, 2), size=self._size), Ship(1, tp=randint(1, 2), size=self._size)]
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
        self._upd_pole()

    def get_ships(self):
        return self._ships

    def _upd_pole(self):
        self._pole = [[0 for _ in range(self._size)] for _ in range(self._size)]
        for ship in self._ships:
            x_0, y_0 = ship.get_start_coords()
            turn, not_turn = ship._turn, ship._not_turn
            c = 0
            for cell_ship in ship:
                self._pole[y_0 + c * turn][x_0 + c * not_turn] = cell_ship
                c += 1

    def get_pole(self):
        return tuple(tuple(x) for x in self._pole)

    def show(self):
        for line in self._pole:
            print(*line)

    def _can_move(self, ship: Ship, distance: int):
        if not ship._is_move:
            return False
        last_ships = [l_ship for l_ship in self._ships if l_ship != ship]
        go_ship = Ship(ship._length, ship._tp, ship._x, ship._y, size=self._size)
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
        self._upd_pole()


# SIZE_GAME_POLE = 7  # constanta
# ship_1 = Ship(4, tp=2, x=1, y=1)
# ship_2 = Ship(2, tp=2, x=3, y=2)
# ship_1.cells_ship_id()
# ship_1.cells_around_ship_id()
# pprint(ship_1._ship_cells)
# pprint(ship_1._around_ship)
# print(ship_1.is_out_pole())
# print(ship_1.is_collide(ship_2))
pole = GamePole(8)
pole.init()
print(pole.get_ships())
pole.show()
pole.move_ships()
print()
pole.show()
print()
print(pole.get_ships())


ship = Ship(2)
ship = Ship(2, 1)
ship = Ship(3, 2, 0, 0)

assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
assert ship._cells == [1, 1, 1], "неверный список _cells"
assert ship._is_move, "неверное значение атрибута _is_move"

ship.set_start_coords(1, 2)
assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"

ship.move(1)
s1 = Ship(4, 1, 0, 0)
s2 = Ship(3, 2, 0, 0)
s3 = Ship(3, 2, 0, 2)

assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
assert s1.is_collide(
    s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"

s2 = Ship(3, 2, 1, 1)
assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"

s2 = Ship(3, 1, 8, 1)
assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"

s2 = Ship(3, 2, 1, 5)
assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"

s2[0] = 2
assert s2[0] == 2, "неверно работает обращение ship[indx]"

p = GamePole(10)
p.init()
for nn in range(5):
    for s in p._ships:
        assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"

        for ship in p.get_ships():
            if s != ship:
                assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
    p.move_ships()

gp = p.get_pole()
assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"

pole_size_8 = GamePole(8)
pole_size_8.init()
