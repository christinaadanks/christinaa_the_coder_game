import pygame

from game.backgrounds import Background
from game.game_data import levels
from game.imports import import_graphics


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
        self.frames = import_graphics('graphics_files/fruits/Cherries.png')
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
    def __init__(self, curr_level, max_level, surface, start_level):
        # overworld setup
        self.display_surface = surface
        self.max_level = max_level
        self.curr_level = curr_level
        self.start_level = start_level

        # sprites
        self.nodes = pygame.sprite.Group()
        self.icon = pygame.sprite.GroupSingle()
        self.background = Background()
        self.setup_nodes()
        self.setup_icon()

        # directions for game menu
        self.font = pygame.font.Font('graphics_files/font/emu.ttf', 8)
        self.dir_surf = self.font.render('press SPACE or ENTER to begin level', True, 'black')
        self.dir_rect = self.dir_surf.get_rect(center=(160, 80))
        self.dir_surf2 = self.font.render('press ESC to exit level & return to menu', True, 'black')
        self.dir_rect2 = self.dir_surf.get_rect(center=(160, 90))
        self.dir_surf3 = self.font.render('use left & right arrows to move player', True, 'black')
        self.dir_rect3 = self.dir_surf.get_rect(center=(160, 110))
        self.dir_surf4 = self.font.render('press space to jump', True, 'black')
        self.dir_rect4 = self.dir_surf.get_rect(center=(160, 120))
        self.dir_surf5 = self.font.render('goal is to collect fruits & reach trophy checkpoint', True, 'black')
        self.dir_rect5 = self.dir_surf.get_rect(center=(160, 130))
        self.dir_surf6 = self.font.render('player dies if they fall off or lose all health', True, 'black')
        self.dir_rect6 = self.dir_surf.get_rect(center=(160, 140))
        self.font = pygame.font.Font('graphics_files/font/emu.ttf', 12)
        self.quit_surf = self.font.render('press ESC to quit', True, 'black')
        self.quit_rect = self.dir_surf.get_rect(center=(260, 300))

    def setup_nodes(self):
        """
        Setup for the level nodes
        """
        for index, node_val in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_val['node'], 'unlocked', node_val['level_graphics'])
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_val['node'], 'locked', node_val['level_graphics'])
            self.nodes.add(node_sprite)

    def setup_icon(self):
        """
        Set up the icons for the levels
        """
        icon_sprite = Icon(self.nodes.sprites()[self.curr_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        """
        Input for moving the cherry (left/right to move from level to leve, space OR return to play level)
        """
        clock = pygame.time.Clock()
        clock.tick(10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.curr_level < self.max_level:
            self.curr_level += 1
        elif keys[pygame.K_LEFT] and self.curr_level > 0:
            self.curr_level -= 1
        elif keys[pygame.K_SPACE]:
            self.start_level(self.curr_level)
        elif keys[pygame.K_RETURN]:
            self.start_level(self.curr_level)
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()

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
        self.display_surface.blit(self.dir_surf, self.dir_rect)
        self.display_surface.blit(self.dir_surf2, self.dir_rect2)
        self.display_surface.blit(self.dir_surf3, self.dir_rect3)
        self.display_surface.blit(self.dir_surf4, self.dir_rect4)
        self.display_surface.blit(self.dir_surf5, self.dir_rect5)
        self.display_surface.blit(self.dir_surf6, self.dir_rect6)
        self.display_surface.blit(self.quit_surf, self.quit_rect)
