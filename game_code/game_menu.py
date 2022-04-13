import pygame

from game_code.backgrounds import Background
from game_code.game_data import levels
from game_code.imports import import_graphics


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, path):
        super().__init__()
        self.image = pygame.image.load(path)
        if status == 'unlocked':
            self.status = 'unlocked'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        if self.status == 'locked':
            color = (0, 0, 0, 100)
            tint = self.image.copy()
            tint.fill(color, None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.frames = import_graphics('../graphics_files/fruits/Cherries.png')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.rect.center = self.pos


class GameMenu:
    """
    Class for the overworld for game/level management
    """
    def __init__(self, start_level, max_level, surface, create_level):
        # overworld setup
        self.display_surface = surface
        self.max_level = max_level
        self.curr_level = start_level
        self.create_level = create_level

        # sprites
        self.nodes = pygame.sprite.Group()
        self.icon = pygame.sprite.GroupSingle()
        self.background = Background()
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        for index, node_val in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_val['node'], 'unlocked', node_val['level_graphics'])
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_val['node'], 'locked', node_val['level_graphics'])
            self.nodes.add(node_sprite)

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.curr_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        clock = pygame.time.Clock()
        clock.tick(10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.curr_level < self.max_level:
            self.curr_level += 1
        elif keys[pygame.K_LEFT] and self.curr_level > 0:
            self.curr_level -= 1
        elif keys[pygame.K_SPACE]:
            self.create_level(self.curr_level)

    def update_icon(self):
        self.icon.sprite.pos = self.nodes.sprites()[self.curr_level].rect.center

    def run(self):
        self.input()
        self.background.draw(self.display_surface)
        self.update_icon()
        self.icon.update()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)