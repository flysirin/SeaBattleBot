from services.SeaBattle import Game
from services.battle_board_image import BattleBoardImage
from PIL import Image
from random import randint, choice


def game_action(x_owner_hit=None, y_owner_hit=None,
                owner_field: Game = None,
                enemy_field: Game = None) -> Image:
    enemy_field.damage_register(x_owner_hit, y_owner_hit)
    do_bot_action_hit_level_2(owner_field)

    enemy_field.move_ships()
    owner_field.move_ships()

    image_left_from_enemy = BattleBoardImage(grid_size=enemy_field.size)
    image_right_from_owner = BattleBoardImage(grid_size=enemy_field.size)

    right_field_from_owner = owner_field.get_field_for_owner()
    left_field_from_enemy = enemy_field.get_field_for_enemy()

    for y, row in enumerate(left_field_from_enemy, 1):
        for x, cell in enumerate(row, 1):
            if cell == 2:
                image_left_from_enemy.draw_hit(x, y)
            elif cell == 3:
                image_left_from_enemy.draw_miss(x, y)

    for y, row in enumerate(right_field_from_owner, 1):
        for x, cell in enumerate(row, 1):
            if cell == 2:
                image_right_from_owner.draw_ship(x, y)
                image_right_from_owner.draw_hit(x, y)
            elif cell == 3:
                image_right_from_owner.draw_miss(x, y)
            elif cell == 1:
                image_right_from_owner.draw_ship(x, y)

    image = image_left_from_enemy.compare_two_images(image_right_from_owner)
    return image


def do_bot_action_hit_level_2(user_game_field: Game):
    # if not damages ships
    if not user_game_field.damage_cells and user_game_field.alive_ship_list \
            and user_game_field.support_free_cells:
        cell_id = choice(list(user_game_field.support_free_cells))
        ship = user_game_field.damage_register(cell_id=cell_id)
        if ship:
            if ship.is_death():
                remove_cells_death_ship(user_game_field, ship)


    # damage ship
    elif user_game_field.alive_ship_list:
        if len(user_game_field.damage_cells) == 1:
            next_cell_id = get_next_hit_by_one_damage_cell(game_field=user_game_field)
            if next_cell_id is None:
                next_cell_id = choice(list(user_game_field.support_free_cells))

            ship = user_game_field.damage_register(cell_id=next_cell_id)
            if ship and ship.is_death():
                remove_cells_death_ship(user_game_field, ship)

        elif 1 < len(user_game_field.damage_cells):
            next_cell_id = get_next_hit_by_few_damage_cells(game_field=user_game_field)

            if next_cell_id is None:
                next_cell_id = choice(list(user_game_field.support_free_cells))

            ship = user_game_field.damage_register(cell_id=next_cell_id)
            if ship and ship.is_death():
                remove_cells_death_ship(user_game_field, ship)

    elif not user_game_field.alive_ship_list:
        return True


def get_next_hit_by_one_damage_cell(game_field: 'Game') -> int | None:
    damage_cell_id = list(game_field.damage_cells)[0]

    possible_next_cells = [damage_cell_id + 1, damage_cell_id - 1,
                           damage_cell_id + 10, damage_cell_id - 10]
    for next_cell_id in possible_next_cells:
        if next_cell_id in game_field.support_free_cells:
            return next_cell_id


def get_next_hit_by_few_damage_cells(game_field: 'Game') -> int | None:
    cell_ids: list = sorted(game_field.damage_cells)
    next_cell_id = None
    if cell_ids[1] - cell_ids[0] == 1:
        next_cell_id = max(cell_ids) + 1
        if next_cell_id not in game_field.support_free_cells:
            next_cell_id = min(cell_ids) - 1

    elif cell_ids[1] - cell_ids[0] == game_field.size:
        next_cell_id = max(cell_ids) + game_field.size
        if next_cell_id not in game_field.support_free_cells:
            next_cell_id = min(cell_ids) - game_field.size

    if next_cell_id in game_field.support_free_cells:
        return next_cell_id


def remove_cells_death_ship(game_field: 'Game', ship: 'Ship') -> None:
    for cell_id in ship._around_ship:
        if cell_id in game_field.support_free_cells:
            game_field.support_free_cells.remove(cell_id)
    length_ship = len(game_field.damage_cells)
    if length_ship in game_field.alive_ship_list:
        game_field.alive_ship_list.remove(length_ship)
    game_field.damage_cells.clear()
    print(ship._around_ship)


game_1 = Game(10)
game_2 = Game(10)
game_1.init()
game_2.init()

image1 = None
for i in range(70):
    image1 = game_action(randint(1, 10), randint(1, 10),
                         game_1, game_2)
    game_1.move_ships()
    game_2.move_ships()
image1.save('image1.png')
print(game_1.support_free_cells)
print(game_1.alive_ship_list)
