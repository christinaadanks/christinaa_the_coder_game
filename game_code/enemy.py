import pygame
from game_code.tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        # use random speed for enemy
        self.speed = randint(1, 3)

    def move(self):
        """
        Move the enemy
        """
        self.rect.x += self.speed

    def reverse_image(self):
        """
        Reverse the image if it is moving right (facing right)
        """
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse_direction(self):
        """
        Reverse the speed when enemy hits constraint
        """
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
