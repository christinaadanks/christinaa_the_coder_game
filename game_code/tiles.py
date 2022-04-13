import pygame
from imports import import_graphics


class Tile(pygame.sprite.Sprite):
    """
    Class for the tiles in the world
    """
    def __init__(self, size, x, y):
        """
        Initialize tile setup
        Args:
            size: size of the tiles (currently set at 32px)
            x: x position (x,y)
            y: y position (x,y)
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        """
        Update the screen location to shift with the player
        Args:
            shift: value to shift the screen (use neg to go right)
        """
        self.rect.x += shift


class GraphicTiles(Tile):
    """
    Class to fill tiles with graphics_files
    """
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        # instead of fill with color, fill with tile graphic
        self.image = surface


class Box(GraphicTiles):
    """
    Class for single tile 'box'
    """
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../graphics_files/boxes/box.png').convert_alpha())


class AnimatedTile(Tile):
    """
    Class for the animated tiles
    """
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_graphics(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Fruit(AnimatedTile):
    """
    Class to make sure fruit is centered in the tiles
    """
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value

