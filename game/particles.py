import pygame

from game.imports import import_graphics


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, category):
        """
        Initialize particles set up
        Args:
            pos: position of the particle
            category: category of enemy
        """
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if category == 'slime_hit':
            self.frames = import_graphics('graphics_files/characters/enemy/hit/slime.png')
        if category == 'duck_hit':
            self.frames = import_graphics('graphics_files/characters/enemy/hit/duck.png')
        if category == 'rabbit_hit':
            self.frames = import_graphics('graphics_files/characters/enemy/hit/rabbit.png')
        if category == 'ghost_hit':
            self.frames = import_graphics('graphics_files/characters/enemy/hit/ghost.png')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Particle animation
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift
