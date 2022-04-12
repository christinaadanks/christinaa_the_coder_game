import pygame
from game_code.imports import import_graphics


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # animations
        self.frames = self.import_player_graphics()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['player_idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

        # player functionality
        self.gravity = 0.95
        self.jump_speed = -8
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4

        # player status
        self.status = 'player_idle'

    def import_player_graphics(self):
        """
        Import graphics for the player
        Returns:
            dictionary of player animations + their graphics
        """
        player_path = '../graphics_files/characters/player/'
        self.animations = {'player_idle': [], 'player_run': [], 'player_jump': [], 'player_fall': []}

        for animation in self.animations.keys():
            full_path = player_path + animation + '.png'
            self.animations[animation] = import_graphics(full_path)

        return self.animations

    def animate(self):
        """
        Animate the player
        """
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def get_input(self):
        """
        Keyboard inputs from user for game play
        """
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1

        if keys[pygame.K_SPACE]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'player_jump'
        elif self.direction.y > 0:
            self.status = 'player_fall'
        else:
            if self.direction.x != 0:
                self.status = 'player_run'
            else:
                self.status = 'player_idle'

    def get_gravity(self):
        """
        Add gravity so player falls
        """
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """
        Jump function for the player
        """
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()