from csv import reader
import pygame
from game.settings import *


def import_csv_data(path):
    """
    Import csv data from Tiled files
    Args:
        path: which file we are importing
    Returns: list of data
    """
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_graphics(path):
    """
    Import graphics
    Args:
        path: which graphics we are importing
    Returns:
    """
    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_y = int(surface.get_size()[1] / TILE_SIZE)

    split_tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            new_surface = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert_alpha()
            new_surface.fill((0, 0, 0, 0))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            split_tiles.append(new_surface)
    return split_tiles
