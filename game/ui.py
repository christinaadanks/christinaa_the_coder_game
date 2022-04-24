import pygame


class UI:
    def __init__(self, surface):
        # UI setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('graphics_files/characters/player/health.png')
        self.health_bar_tl = (28, 20)
        self.health_max_w = 100
        self.health_h = 8

        # fruits
        self.fruits = pygame.image.load('graphics_files/fruits/fruits_bar.png')
        self.fruits_rect = self.fruits.get_rect(topleft=(22, 50))
        self.font = pygame.font.Font('graphics_files/font/emu.ttf', 11)

    def display_health(self, curr, full):
        """
        Display the health bar in the game
        Args:
            curr: current health status
            full: full health status [100]
        """
        self.display_surface.blit(self.health_bar, (20, 20))
        # get percentage (in case full health # changes)
        curr_ratio = curr / full
        curr_bar_w = self.health_max_w * curr_ratio
        health_bar_rect = pygame.Rect(self.health_bar_tl, (curr_bar_w, self.health_h))
        if curr_ratio > 0.5:
            pygame.draw.rect(self.display_surface, '#7DE500', health_bar_rect)
        elif 0.5 >= curr_ratio > 0.25:
            pygame.draw.rect(self.display_surface, '#FEBF2D', health_bar_rect)
        else:
            pygame.draw.rect(self.display_surface, '#FF4864', health_bar_rect)

    def display_fruits(self, balance):
        """
        Display the fruit balance in the game
        Args:
            balance: number of points from the fruits collected
        """
        self.display_surface.blit(self.fruits, self.fruits_rect)
        fruit_balance = self.font.render(str(balance), False, 'black')
        # set font centered with the fruit icon
        fruit_balance_rect = fruit_balance.get_rect(midleft=(self.fruits_rect.right + 10, self.fruits_rect.centery))
        self.display_surface.blit(fruit_balance, fruit_balance_rect)