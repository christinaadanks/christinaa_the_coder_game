import pygame

from game_code.settings import *


class GameOver:
    """
    Class for game over state
    """
    def __init__(self, curr_level, surface, start_level, open_menu):
        # game over setup
        self.display_surface = surface
        self.start_level = start_level
        self.open_menu = open_menu
        self.curr_level = curr_level

        # game over display
        self.font = pygame.font.Font('../graphics_files/font/emu.ttf', 20)
        self.game_over_surf = self.font.render('GAME OVER', True, 'white')
        self.game_over_rect = self.game_over_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.font = pygame.font.Font('../graphics_files/font/emu.ttf', 10)
        self.play_again_surf = self.font.render('PLAY AGAIN? y/n', True, 'white')
        self.play_again_rect = self.play_again_surf.get_rect(topleft=(380, 100))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            self.start_level(self.curr_level)
        elif keys[pygame.K_n]:
            self.open_menu(0, 0)

    def run(self):
        self.input()
        self.display_surface.blit(self.game_over_surf, self.game_over_rect)
        self.display_surface.blit(self.play_again_surf, self.play_again_rect)
