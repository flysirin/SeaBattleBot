from PIL import Image, ImageDraw, ImageFont


def create_sea_battle_board(cell_size=50, grid_size=10):
    img_size = cell_size * (grid_size + 1)
    img = Image.new('RGB', (img_size, img_size), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", cell_size // 2)
    except IOError:
        font = ImageFont.load_default()

    for i in range(grid_size + 1):
        draw.line([(i * cell_size + cell_size, cell_size),
                   (i * cell_size + cell_size, img_size)], fill='black')
        draw.line([(cell_size, i * cell_size + cell_size),
                   (img_size, i * cell_size + cell_size)], fill='black')

    for i in range(grid_size):
        letter = chr(ord('A') + i)
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        text_x = (i + 1) * cell_size + (cell_size - text_size[0]) // 2
        text_y = (cell_size - text_size[1]) // 2
        draw.text((text_x, text_y), letter, fill='black', font=font)

    for i in range(grid_size):
        number = str(i + 1)
        bbox = draw.textbbox((0, 0), number, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        text_x = (cell_size - text_size[0]) // 2
        text_y = (i + 1) * cell_size + (cell_size - text_size[1]) // 2
        draw.text((text_x, text_y), number, fill='black', font=font)

    return img


def draw_ship(draw, x, y, cell_size):
    draw.line([(x, y), (x + cell_size, y + cell_size)], fill='red', width=3)
    draw.line([(x, y + cell_size), (x + cell_size, y)], fill='red', width=3)


def draw_hit(draw, x, y, cell_size):
    draw.ellipse([(x + cell_size // 4, y + cell_size // 4),
                  (x + 3 * cell_size // 4, y + 3 * cell_size // 4)], outline='red', width=3)


def draw_miss(draw, x, y, cell_size):
    draw.rectangle([(x, y), (x + cell_size, y + cell_size)], fill='gray')


# Генерация и сохранение изображения
board_image = create_sea_battle_board()
draw = ImageDraw.Draw(board_image)

# Пример рисования попадания, мимо и части корабля
cell_size = 50
# Координаты клетки A1
x1, y1 = cell_size, cell_size * 2
# Координаты клетки B2
x2, y2 = cell_size * 2, cell_size * 3
# Координаты клетки C3
x3, y3 = cell_size * 3, cell_size * 4

draw_hit(draw, x1, y1, cell_size)
draw_miss(draw, x2, y2, cell_size)
draw_ship(draw, x3, y3, cell_size)

board_image.save('sea_battle_board_with_marks.png')
