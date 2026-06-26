import pygame
from code.Const import (PLAYER_SPEED, PLAYER_JUMP, PLAYER_GRAVITY, WIN_WIDTH, TILE_SIZE)
from code.Entity import Entity


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

    def update(self, keys, collision_map):
        self.move(keys)
        self.horizontal_collision(collision_map)
        self.apply_gravity()
        self.vertical_collision(collision_map)

    def move(self, keys):
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED

        self.rect.x += self.velocity_x

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH

    def jump(self):
        if self.on_ground:
            self.velocity_y = PLAYER_JUMP
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y

    def is_solid(self, collision_map, tile_x, tile_y):
        if tile_x < 0:
            return False
        if tile_y < 0:
            return False
        if tile_y >= len(collision_map):
            return False
        if tile_x >= len(collision_map[0]):
            return False
        return collision_map[tile_y][tile_x] == 1

    def horizontal_collision(self, collision_map):
        top_tile = self.rect.top // TILE_SIZE
        bottom_tile = (self.rect.bottom - 1) // TILE_SIZE

        # andando para direita
        if self.velocity_x > 0:
            tile_x = self.rect.right // TILE_SIZE
            for tile_y in range(top_tile, bottom_tile + 1):
                if self.is_solid(collision_map, tile_x, tile_y):
                    self.rect.right = tile_x * TILE_SIZE
                    break

        # andando para esquerda
        elif self.velocity_x < 0:
            tile_x = self.rect.left // TILE_SIZE
            for tile_y in range(top_tile, bottom_tile + 1):
                if self.is_solid(collision_map, tile_x, tile_y):
                    self.rect.left = (tile_x + 1) * TILE_SIZE
                    break

    def vertical_collision(self, collision_map):
        self.on_ground = False
        left_tile = self.rect.left // TILE_SIZE
        right_tile = (self.rect.right - 1) // TILE_SIZE

        # caindo
        if self.velocity_y > 0:
            tile_y = self.rect.bottom // TILE_SIZE
            for tile_x in range(left_tile, right_tile + 1):
                if self.is_solid(collision_map, tile_x, tile_y):
                    self.rect.bottom = tile_y * TILE_SIZE
                    self.velocity_y = 0
                    self.on_ground = True
                    break

        # subindo
        elif self.velocity_y < 0:
            tile_y = self.rect.top // TILE_SIZE
            for tile_x in range(left_tile, right_tile + 1):
                if self.is_solid(collision_map, tile_x, tile_y):
                    self.rect.top = (tile_y + 1) * TILE_SIZE
                    self.velocity_y = 0
                    break
