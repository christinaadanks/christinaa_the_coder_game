import sys
import pygame
from game_code.settings import *
from game_code.level import Level
from game_code.game_menu import GameMenu
from game_code.ui import UI


class Game:
    """
    Class for the main game
    """
    def __init__(self):
        # main game
        self.level = None
        self.status = 'game_menu'
        self.max_level = 3
        self.game_menu = GameMenu(0, self.max_level, screen, self.start_level)

        # player statuses
        self.max_health = 100
        self.curr_health = 100
        self.fruits = 0

        # UI
        self.ui = UI(screen)

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
        """
        Start the current level
        Args:
            curr_level: current level
        """
        self.status = 'level'
        new_screen = self.screen_dimensions()
        self.level = Level(curr_level, new_screen, self.open_menu, self.update_fruits, self.update_health)

    def open_menu(self, curr_level, new_max_level):
        """
        Open the level menu
        Args:
            curr_level: current level
            new_max_level: max level (unlocks new levels each time you win)
        """
        self.status = 'game_menu'
        new_screen = self.screen_dimensions()
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.game_menu = GameMenu(curr_level, self.max_level, new_screen, self.start_level)

    def update_fruits(self, balance):
        self.fruits += balance

    def update_health(self, amount):
        self.curr_health += amount

    def run(self):
        """
        Run game depending on the status
        """
        if self.status == 'game_menu':
            self.game_menu.run()
        else:
            self.level.run()
            self.ui.display_health(self.curr_health, self.max_health)
            self.ui.display_fruits(self.fruits)


# full game setup
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
    clock.tick(50)
