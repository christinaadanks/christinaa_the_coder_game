import pygame


class Tile(pygame.sprite.Sprite):
    """
    Class for the tiles in the world
    """
    def __init__(self, size, x, y):
        """
        Initiliaze tile setup
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
    Class to fill tiles with graphics
    """
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        # instead of fill with color, fill with tile graphic
        self.image = surface

