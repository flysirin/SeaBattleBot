from random import randint, choice
import pygame
import sys
from string import ascii_uppercase as asci
from Sea_battle import Ship, GamePole


pygame.init()

size = (1510, 530)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game field")
width, height = 40, 40
margin = 10
padding = 20
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (10, 100, 255)
COLOR_1 = (150, 50, 50)
massive = [[0]*10 for _ in range(10)]

game_pole_1 = GamePole(10)
game_pole_1.init()
game_pole_2 = GamePole(10)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            print(f"x={x_mouse}, y={y_mouse}, (x_mouse-padding)//(margin+width){(x_mouse-padding),(margin+width)}")
            column = (x_mouse-padding)//(margin+width)
            row = (y_mouse-padding)//(margin+height)

            try:
                if padding + margin < x_mouse < (width + margin)*10 + padding and\
                        padding + margin < y_mouse < (width + margin)*10 + padding:

                    massive[row][column] ^= 1      # '^' - побитовое умножение

            except IndexError:
                continue

    for i in range(10):   # render text coordinate
        font = pygame.font.SysFont("stxingkai", 30)
        text_1 = font.render(asci[i], True, BLUE)
        screen.blit(text_1, (i * (width + margin) + padding + width // 2 + margin // 3, 5))
        text_2 = font.render(str(i+1), True, BLUE)
        screen.blit(text_2, (5, i * (height + margin) + padding + height // 2 + margin // 3))

    massive = [list(row) for row in game_pole_1.get_pole()]
    for row in range(10):
        for col in range(10):
            if massive[row][col] == 1:
                color = COLOR_1
            else:
                color = WHITE
            x = col * width + (col + 1) * margin + padding
            y = row * height + (row + 1) * margin + padding
            pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.display.update()
