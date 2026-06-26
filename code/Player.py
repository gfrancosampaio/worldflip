import pygame.key

from code.Const import PLAYER_SPEED, WIN_WIDTH, PLAYER_JUMP, PLAYER_GRAVITY
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position:tuple):
        super().__init__(name,position)
        self.velocity_y = 0
        self.on_ground = True

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            if self.rect.right < WIN_WIDTH:
                self.rect.x += PLAYER_SPEED

    def jump(self):
        if self.on_ground:
            self.velocity_y = PLAYER_JUMP
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += PLAYER_GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.bottom >= 400:
            self.rect.bottom = 400
            self.velocity_y = 0
            self.on_ground = True
