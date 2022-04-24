import sys
import time

import pygame

from game.game_over import GameOver
from game.music import Music
from game.settings import *
from game.level import Level
from game.game_menu import GameMenu
from game.ui import UI


class Game:
    """
    Class for the main game
    """
    def __init__(self):
        # sounds
        self.menu_music = pygame.mixer.Sound('../sounds/menu.mp3')
        self.menu_music.set_volume(0.5)
        self.level_music = Music()
        self.death_sound = pygame.mixer.Sound('../sounds/death.wav')

        # main game
        self.level = None
        self.status = 'game_menu'
        self.max_level = 1
        self.game_menu = GameMenu(0, self.max_level, screen, self.start_level)
        self.menu_music.play(loops=-1)
        self.game_over = None

        # player statuses
        self.curr_level = 0
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
        self.menu_music.stop()
        self.level_music.stop()
        self.level_music.play()
        if self.curr_health < 100:
            self.curr_health = 100
        if self.fruits > 0:
            self.fruits = 0
        self.status = 'level'
        new_screen = self.screen_dimensions()
        self.level = Level(curr_level, new_screen, self.open_menu, self.update_fruits, self.update_health,
                           self.open_game_over, self.update_level)

    def open_menu(self, curr_level, new_max_level):
        """
        Open the level menu
        Args:
            curr_level: current level
            new_max_level: max level (unlocks new levels each time you win)
        """
        self.level_music.stop()
        self.status = 'game_menu'
        new_screen = self.screen_dimensions()
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.game_menu = GameMenu(curr_level, self.max_level, new_screen, self.start_level)
        self.menu_music.play(loops=-1)

    def open_game_over(self, curr_level):
        time.sleep(2)
        self.level_music.unpause()
        self.status = 'game_over'
        new_screen = self.screen_dimensions()
        self.game_over = GameOver(curr_level, new_screen, self.start_level, self.open_menu)

    def update_fruits(self, balance):
        self.fruits += balance

    def update_health(self, amount):
        self.curr_health += amount

    def update_level(self, level):
        self.curr_level += level

    def run(self):
        """
        Run game depending on the status
        """
        if self.status == 'game_menu':
            self.game_menu.run()
        elif self.status == 'game_over':
            self.game_over.run()
        else:
            self.level.run()
            self.ui.display_health(self.curr_health, self.max_health)
            self.ui.display_fruits(self.fruits)
            if self.curr_health <= 0:
                self.level_music.pause()
                self.death_sound.play()
                self.open_game_over(self.curr_level)


# full game setup
pygame.init()
# default game screen will be menu size
screen = pygame.display.set_mode((int(WIDTH/2), HEIGHT))
clock = pygame.time.Clock()
# set title of game
pygame.display.set_caption("🍒 the pink coder")
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
