import pygame
from game_code.imports import import_graphics


class Player(pygame.sprite.Sprite):
    def __init__(self, position, surface, update_health):
        super().__init__()
        # animations
        self.animations = {'player_idle': [], 'player_run': [], 'player_jump': [], 'player_fall': [], 'player_hit': []}
        self.frames = self.import_player_graphics()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['player_idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

        # player functionality
        self.gravity = 0.8
        self.jump_speed = -15
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.update_health = update_health
        self.damage_delay = False
        self.damage_delay_duration = 1000
        self.collision_time = 0

        # player status
        self.status = 'player_idle'
        self.direction_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_player_graphics(self):
        """
        Import graphics for the player
        Returns:
            dictionary of player animations + their graphics
        """
        player_path = '../graphics_files/characters/player/'

        for animation in self.animations.keys():
            full_path = player_path + animation + '.png'
            self.animations[animation] = import_graphics(full_path)

        return self.animations

    def animate(self):
        """
        Animate the player
        """
        animation = self.animations[self.status]

        # iterate through the animation list for the frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # reverse image if moving left
        image = animation[int(self.frame_index)]
        if self.direction_right:
            self.image = image
        else:
            rev_image = pygame.transform.flip(image, True, False)
            self.image = rev_image

        # setting the rectangle (possible scenarios for player on the ground
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        """
        Keyboard inputs from user for game play
        """
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.direction_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.direction_right = False

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        """
        Get status of what the player is doing dependent on x/y direction
        """
        if self.damage_delay:
            self.status = 'player_hit'
        elif self.direction.y < 0:
            self.status = 'player_jump'
        elif self.direction.y > 1:
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

    def get_damage(self):
        if not self.damage_delay:
            self.update_health(-100)
            self.damage_delay = True
            self.collision_time = pygame.time.get_ticks()

    def damage_timer(self):
        if self.damage_delay:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.collision_time >= self.damage_delay_duration:
                self.damage_delay = False

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.damage_timer()