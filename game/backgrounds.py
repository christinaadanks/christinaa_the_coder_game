import pygame
from game.settings import *
from random import choice, randint
from game.tiles import GraphicTiles


class Background:
    def __init__(self):
        self.image = pygame.image.load('../graphics_files/backgrounds/sky.png')
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

    def draw(self, surface):
        surface.blit(self.image, (0, 0))


class Clouds:
    def __init__(self, ground, width, clouds):
        cloud_list = []
        image1 = pygame.image.load('../graphics_files/backgrounds/cloud1.png')
        image2 = pygame.image.load('../graphics_files/backgrounds/cloud2.png')
        image3 = pygame.image.load('../graphics_files/backgrounds/cloud3.png')
        cloud_list.append(image1)
        cloud_list.append(image2)
        cloud_list.append(image3)

        min_x = -WIDTH
        max_x = width + WIDTH
        min_y = 0
        max_y = ground

        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(clouds):
            cloud = choice(cloud_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = GraphicTiles(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)