from PIL import Image, ImageDraw, ImageFont


class BattleBoardImage:
    def __init__(self, cell_size=50, grid_size=10):
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.board_img = self._create_sea_battle_board()
        self.draw = ImageDraw.Draw(self.board_img)

    def _create_sea_battle_board(self) -> Image:
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

    def draw_hit(self, n_col, n_row):
        x, y = self.cell_size * n_col, self.cell_size * n_row
        self.draw.line([(x, y), (x + self.cell_size, y + self.cell_size)], fill='red', width=3)
        self.draw.line([(x, y + self.cell_size), (x + self.cell_size, y)], fill='red', width=3)

    def draw_miss(self, n_col, n_row, radius=5):
        x, y = self.cell_size * n_col, self.cell_size * n_row
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        self.draw.ellipse([(center_x - radius, center_y - radius),
                      (center_x + radius, center_y + radius)], outline='blue', width=2, fill='blue')

    def draw_ship(self, n_col, n_row):
        x, y = self.cell_size * n_col, self.cell_size * n_row
        self.draw.rectangle([(x, y), (x + self.cell_size, y + self.cell_size)], fill='gray', outline='blue', width=2)
        # draw.rectangle([(x, y), (x + cell_size, y + cell_size)], outline='black', width=3)

    @property
    def get_image(self):
        return self.board_img

    def compare_two_images(self, board_image_2: 'BattleBoardImage') -> Image:
        width, height = self.board_img.size
        new_width, new_height = 2 * width, height
        new_image = Image.new('RGB', (new_width, new_height), 'white')
        new_image.paste(self.board_img, (0, 0))
        new_image.paste(board_image_2.get_image, (width, 0))
        return new_image


# image_1 = BattleBoardImage(50, 10)
# image_1.draw_hit(1, 2)
# image_1.draw_hit(10, 9)
# image_1.draw_miss(10, 2)
#
# image_2 = BattleBoardImage(50, 10)
# image_2.draw_hit(10, 10)
# image_2.draw_hit(9, 9)
# image_2.draw_miss(8, 8)
# img = image_1.compare_two_images(image_2)
#
# img.save('images.png')
