import pygame
import sys
import pygame

from game_code.settings import *
from game_code.level import Level
from game_code.game_data import level_0
from game_code.game_menu import GameMenu


class Game:
    """
    Class for the main game
    """
    def __init__(self):
        self.status = 'game_menu'
        self.max_level = 0
        self.game_menu = GameMenu(0, self.max_level, screen, self.start_level)

    def screen_dimensions(self):
        """
        Update the dimensions of the game screen depending on game mode
        """
        if self.status == 'game_menu':
            display_screen = pygame.display.set_mode((int(WIDTH/2), HEIGHT))
        else:
            display_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        return display_screen

    def start_level(self, curr_level):
        self.status = 'level'
        new_screen = self.screen_dimensions()
        self.level = Level(curr_level, new_screen, self.open_menu)

    def open_menu(self, curr_level, new_max_level):
        self.status = 'game_menu'
        new_screen = self.screen_dimensions()
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.game_menu = GameMenu(curr_level, self.max_level, new_screen, self.start_level)

    def run(self):
        if self.status == 'game_menu':
            self.game_menu.run()
        else:
            self.level.run()


pygame.init()
# default game screen will be menu size
screen = pygame.display.set_mode((int(WIDTH/2), HEIGHT))
clock = pygame.time.Clock()
# set title of game
pygame.display.set_caption("Christinaa The Pink Coder")
# create game
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    # run game
    game.run()

    pygame.display.update()
    clock.tick(60)
