import pygame.key

from code.Const import PLAYER_SPEED, WIN_WIDTH, PLAYER_JUMP, PLAYER_GRAVITY, TILE_SIZE
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position:tuple):
        super().__init__(name,position)
        self.velocity_y = 0
        self.on_ground = True

    def move(self, keys):
        # Moving left
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= PLAYER_SPEED

        # Moving right
        if keys[pygame.K_RIGHT]:
            if self.rect.right < WIN_WIDTH:
                self.rect.x += PLAYER_SPEED

    def jump(self):
        if self.on_ground:
            self.velocity_y = PLAYER_JUMP
            self.on_ground = False

    def apply_gravity(self, collision_map):

        #gravity
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y

        # actual_tile
        tile_x = self.rect.centerx // TILE_SIZE
        tile_y = self.rect.bottom // TILE_SIZE

        # tile limits
        if tile_y >= len(collision_map):
            return

        # ground collision
        if collision_map[tile_y][tile_x] == 1:
            self.rect.bottom = tile_y * TILE_SIZE
            self.velocity_y = 0
            self.on_ground = True
