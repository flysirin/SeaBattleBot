from services.SeaBattle import Game
from services.battle_board_image import BattleBoardImage
from PIL import Image
from random import randint


def game_action(x_owner_hit=None, y_owner_hit=None,
                x_enemy_hit=None, y_enemy_hit=None,
                owner_field: Game = None,
                enemy_field: Game = None) -> Image:
    enemy_field.damage_register(x_owner_hit, y_owner_hit)
    owner_field.damage_register(x_enemy_hit, y_enemy_hit)
    enemy_field.move_ships()
    owner_field.move_ships()

    image_right_from_enemy = BattleBoardImage(grid_size=enemy_field.size)
    image_left_from_owner = BattleBoardImage(grid_size=enemy_field.size)

    right_field_from_enemy = enemy_field.get_field_for_enemy()
    left_field_owner = owner_field.get_field_for_owner()

    for y, row in enumerate(right_field_from_enemy, 1):
        for x, cell in enumerate(row, 1):
            if cell == 2:
                image_right_from_enemy.draw_hit(x, y)
            elif cell == 3:
                image_right_from_enemy.draw_miss(x, y)

    for y, row in enumerate(left_field_owner, 1):
        for x, cell in enumerate(row, 1):
            if cell == 2:
                image_left_from_owner.draw_ship(x, y)
                image_left_from_owner.draw_hit(x, y)
            elif cell == 3:
                image_left_from_owner.draw_miss(x, y)

    image = image_right_from_enemy.compare_two_images(image_left_from_owner)
    return image


game_1 = Game(10)
game_2 = Game(10)
game_1.init()
game_2.init()

image1 = None
for i in range(400):
    image1 = game_action(randint(1, 10), randint(1, 10),
                randint(1, 10), randint(1, 10),
                         game_1, game_2)

image1.save('image1.png')