import pygame
from game_code.imports import import_csv_data, import_graphics
from game_code.particles import Particle
from game_code.settings import *
from game_code.tiles import Tile, GraphicTiles, Box, Fruit
from game_code.enemy import Enemy
from game_code.player import Player
from game_code.game_data import levels
from game_code.backgrounds import Background, Clouds


class Level:
    """
    Class for handling levels_files
    """
    enemy_status = 'None'

    def __init__(self, curr_level, surface, open_menu, update_fruits, update_health, open_game_over,
                 update_level):
        """
        Initialize level setup
        Args:
            level_data: level data path we are importing from Tiled CSV file
            game_surface: screen the game_code is to be displayed on
        """
        # overall world setup
        self.open_menu = open_menu
        self.curr_level = curr_level
        self.update_level = update_level

        # game over setup
        self.open_game_over = open_game_over
        # get level data
        level_data = levels[self.curr_level]
        self.new_max = level_data['unlock']

        # basic setup
        self.display_surface = surface
        self.display_shift = 0
        self.current_x = 0

        # player
        player_data = import_csv_data(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.Group()
        self.create_player(player_data, update_health)

        # UI
        self.update_fruits = update_fruits

        # hit particles
        self.hit_sprites = pygame.sprite.Group()

        # terrain setup
        terrain_data = import_csv_data(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_data, 'terrain')

        # box setup
        box_data = import_csv_data(level_data['boxes'])
        self.box_sprites = self.create_tile_group(box_data, 'box')

        # fruits
        fruit_data = import_csv_data(level_data['fruits'])
        self.fruit_sprites = self.create_tile_group(fruit_data, 'fruits')

        # enemies
        enemy_data = import_csv_data(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_data, 'enemies')

        # constraints
        constraint_data = import_csv_data(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_data, 'constraints')

        # background
        w = len(fruit_data[0]) * TILE_SIZE
        self.background = Background()
        self.clouds = Clouds(200, w, 25)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.open_menu(self.curr_level, 0)

    ######################## GRAPHICS ########################

    def create_player(self, layout, update_health):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col != '-1':
                    if col == '4':
                        player_sprite = Player((x, y), self.display_surface, update_health)
                        self.player.add(player_sprite)
                    else:
                        goal_surface_list = import_graphics('../graphics_files/characters/player/end.png')
                        goal_surface = goal_surface_list[int(col)]
                        sprite = GraphicTiles(TILE_SIZE, x, y, goal_surface)
                        self.goal.add(sprite)

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
                        terrain_tile_list = import_graphics('../graphics_files/terrain/terrain.png')
                        terrain_surface = terrain_tile_list[int(col)]
                        sprite = GraphicTiles(TILE_SIZE, x, y, terrain_surface)

                    if category == 'box':
                        sprite = Box(TILE_SIZE, x, y)

                    if category == 'fruits':
                        if col == '0':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Apple.png', 1)
                        if col == '17':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Bananas.png', 2)
                        if col == '34':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Cherries.png', 2)
                        if col == '51':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Kiwi.png', 2)
                        if col == '68':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Melon.png', 1)
                        if col == '85':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Orange.png', 1)
                        if col == '102':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Pineapple.png', 1)
                        if col == '119':
                            sprite = Fruit(TILE_SIZE, x, y, '../graphics_files/fruits/Strawberry.png', 1)

                    if category == 'enemies':
                        if col == '1':
                            sprite = Enemy(TILE_SIZE, x, y, '../graphics_files/characters/enemy/slime_enemy.png')
                            self.enemy_status = 'slime'
                        if col == '2':
                            sprite = Enemy(TILE_SIZE, x, y, '../graphics_files/characters/enemy/duck_enemy.png')
                            self.enemy_status = 'duck'
                        if col == '3':
                            sprite = Enemy(TILE_SIZE, x, y, '../graphics_files/characters/enemy/ghost_enemy.png')
                            self.enemy_status = 'ghost'
                        if col == '4':
                            sprite = Enemy(TILE_SIZE, x, y, '../graphics_files/characters/enemy/rabbit_enemy.png')
                            self.enemy_status = 'rabbit'

                    if category == 'constraints':
                        sprite = Tile(TILE_SIZE, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def move_screen(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < WIDTH / 4 and direction_x < 0:
            self.display_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.display_shift = -8
            player.speed = 0
        else:
            self.display_shift = 0
            player.speed = 8

    ######################## COLLISIONS ########################

    def enemy_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse_direction()

    def player_x_collision(self):
        """
        Handle collision b/t player vs objects (boxes + terrain) moving on the x-axis
        """
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # set the sprites that the player can collide with (box + terrain)
        collision_sprites = self.terrain_sprites.sprites() + self.box_sprites.sprites()

        for sprite in collision_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def player_y_collision(self):
        """
        Handle collision b/t player vs objects (boxes + terrain) moving on the y-axis
        """
        player = self.player.sprite
        player.get_gravity()

        # set the sprites that the player can collide with (box + terrain)
        collision_sprites = self.terrain_sprites.sprites() + self.box_sprites.sprites()

        for sprite in collision_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def player_death(self):
        if self.player.sprite.rect.top > HEIGHT:
            self.open_game_over(self.curr_level)

    def player_complete(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.open_menu(self.curr_level + 1, self.new_max)
            self.update_level(1)

    def fruit_collision(self):
        picked_fruits = pygame.sprite.spritecollide(self.player.sprite, self.fruit_sprites, True)
        if picked_fruits:
            for fruit in picked_fruits:
                self.update_fruits(fruit.value)

    def player_enemy_collision(self):
        enemy_collide = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if enemy_collide:
            for enemy in enemy_collide:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                # ranges for enemy kill/player injury
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    # bounce player after kill
                    self.player.sprite.direction.y = -10
                    if self.enemy_status == 'slime':
                        hit_sprite = Particle(enemy.rect.center, 'slime_hit')
                    if self.enemy_status == 'duck':
                        hit_sprite = Particle(enemy.rect.center, 'duck_hit')
                    if self.enemy_status == 'ghost':
                        hit_sprite = Particle(enemy.rect.center, 'ghost_hit')
                    if self.enemy_status == 'rabbit':
                        hit_sprite = Particle(enemy.rect.center, 'rabbit_hit')
                    self.hit_sprites.add(hit_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        """
        Run the level (display the sprites, make sure to put bottom layers first)
        """
        self.input()
        # background
        self.background.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.display_shift)
        # terrain
        self.terrain_sprites.update(self.display_shift)
        self.terrain_sprites.draw(self.display_surface)
        # fruits
        self.fruit_sprites.update(self.display_shift)
        self.fruit_sprites.draw(self.display_surface)
        # enemy
        self.enemy_sprites.update(self.display_shift)
        self.hit_sprites.update(self.display_shift)
        self.hit_sprites.draw(self.display_surface)
        # constraints
        self.constraint_sprites.update(self.display_shift)
        self.enemy_collision()
        self.enemy_sprites.draw(self.display_surface)
        # boxes
        self.box_sprites.update(self.display_shift)
        self.box_sprites.draw(self.display_surface)
        # players finish line
        self.goal.update(self.display_shift)
        self.goal.draw(self.display_surface)
        # move screen w/ player
        self.move_screen()
        # players
        self.player.update()
        self.player_x_collision()
        self.player_y_collision()
        self.player.draw(self.display_surface)
        # collisions
        self.player_death()
        self.player_complete()
        self.fruit_collision()
        self.player_enemy_collision()