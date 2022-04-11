import pygame
from game.imports import import_csv_data, import_graphics
from game.settings import *
from game.tiles import Tile, GraphicTiles


class Level:
    """
    Class for handling levels
    """
    def __init__(self, level_data, game_surface):
        """
        Initialize level setup
        Args:
            level_data: level data path we are importing from Tiled CSV file
            game_surface: screen the game is to be displayed on
        """
        # overall world setup
        self.display_surface = game_surface
        self.display_shift = 0

        # terrain setup
        terrain_data = import_csv_data(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_data, 'terrain')

    def create_tile_group(self, layout, category):
        """
        create tile groups to display in world
        Args:
            layout: data imported from Tiles CSV file
            category: category of data to be imported
        Returns:
            sprite group that was created
        """
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if category == 'terrain':
                        terrain_tile_list = import_graphics('../graphics/terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = GraphicTiles(TILE_SIZE, x, y, tile_surface)
                        sprite_group.add(sprite)
        return sprite_group

    def run(self):
        """
        Run the level
        """
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.display_shift)