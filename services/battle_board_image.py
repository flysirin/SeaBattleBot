from PIL import Image, ImageDraw, ImageFont


class BattleBoardImage:
    def __init__(self, cell_size=50, grid_size=10):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.board_img_1 = self.create_sea_battle_board()
        self.board_img_2 = self.create_sea_battle_board()

    def create_sea_battle_board(self):
        img_size = self.cell_size * (self.grid_size + 1)
        img = Image.new('RGB', (img_size + 25, img_size + 25), 'white')
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", self.cell_size // 2)
        except IOError:
            font = ImageFont.load_default()

        for i in range(self.grid_size + 1):
            draw.line([(i * self.cell_size + self.cell_size, self.cell_size),
                       (i * self.cell_size + self.cell_size, img_size)], fill='black')
            draw.line([(self.cell_size, i * self.cell_size + self.cell_size),
                       (img_size, i * self.cell_size + self.cell_size)], fill='black')

        for i in range(self.grid_size):
            letter = chr(ord('A') + i)
            bbox = draw.textbbox((0, 0), letter, font=font)
            text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
            text_x = (i + 1) * self.cell_size + (self.cell_size - text_size[0]) // 2
            text_y = (self.cell_size - text_size[1]) // 2
            draw.text((text_x, text_y), letter, fill='black', font=font)

        for i in range(self.grid_size):
            number = str(i + 1)
            bbox = draw.textbbox((0, 0), number, font=font)
            text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
            text_x = (self.cell_size - text_size[0]) // 2
            text_y = (i + 1) * self.cell_size + (self.cell_size - text_size[1]) // 2
            draw.text((text_x, text_y), number, fill='black', font=font)

        return img

    def draw_hit(self, draw, n_col, n_row):
        x, y = self.cell_size * n_col, self.cell_size * n_row
        draw.line([(x, y), (x + self.cell_size, y + self.cell_size)], fill='red', width=3)
        draw.line([(x, y + self.cell_size), (x + self.cell_size, y)], fill='red', width=3)

    def draw_miss(self, draw, n_col, n_row, radius=5):
        x, y = self.cell_size * n_col, self.cell_size * n_row
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        draw.ellipse([(center_x - radius, center_y - radius),
                      (center_x + radius, center_y + radius)], outline='blue', width=2, fill='blue')

    def draw_ship(self, draw, n_col, n_row):
        x, y = self.cell_size * n_col, self.cell_size * n_row
        draw.rectangle([(x, y), (x + self.cell_size, y + self.cell_size)], fill='gray', outline='blue', width=2)
        # draw.rectangle([(x, y), (x + cell_size, y + cell_size)], outline='black', width=3)

    def compare_two_images(self):
        width, height = self.board_img_1.size
        new_width, new_height = 2 * width, height
        new_image = Image.new('RGB', (new_width, new_height), 'white')
        new_image.paste(self.board_img_1, (0, 0))
        new_image.paste(self.board_img_2, (width, 0))
        return new_image


image = BattleBoardImage(50, 10)
image.compare_two_images()
# Генерация и сохранение изображения
# board_image_1 = create_sea_battle_board()
# board_image_2 = create_sea_battle_board()

# draw_1 = ImageDraw.Draw(board_image_1)
# draw_2 = ImageDraw.Draw(board_image_2)

# Пример рисования попадания, мимо и части корабля
# self.cell_size = 50
# Координаты клетки A1
x1, y1 = 1, 2
# Координаты клетки B2
x2, y2 = 2, 9
# Координаты клетки C3
x3, y3 = 3, 4

# draw_hit(draw_1, x1, y1, self.cell_size)
# draw_miss(draw_1, x2, y2, self.cell_size)
# draw_ship(draw_1, x3, y3, self.cell_size)
#
# draw_hit(draw_2, x1, y1, self.cell_size)
# draw_miss(draw_2, x2, y2, self.cell_size)
# draw_ship(draw_2, x3, y3, self.cell_size)

# new_img = compare_two_images(board_image_1, board_image_2)

# new_img.save('sea_battle_board.png')
# board_image_1.save('sea_battle_board_with_marks.png')
