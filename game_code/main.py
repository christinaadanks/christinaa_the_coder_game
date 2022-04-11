import pygame
import sys

from game_code.settings import *
from game_code.level import Level
from game_code.game_data import level_0

pygame.init()
# screen size (can update from settings.py)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# set the level we are currently on
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
