import sys

import pygame
from pygame import Surface

from code.Const import COLLISION_MAP_0, COLLISION_MAP_1, WIN_HEIGHT
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Platform import Platform


class Level:
    def __init__(self, window: Surface, name: str):
        self.window = window
        self.name = name

        self.world_state = 0

        self.player = EntityFactory.get_entity('Player')

        self.platform_list: list[Platform] = []
        self.platform_list.extend(EntityFactory.get_entity(self.name + 'Plat'))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.on_ground:
                            self.player.jump()
                            self.world_state = 1 - self.world_state

            keys = pygame.key.get_pressed()
            self.player.move(keys)

            if self.world_state == 0:
                self.player.apply_gravity(COLLISION_MAP_0)
            else:
                self.player.apply_gravity(COLLISION_MAP_1)

            if self.player.rect.top > 450:
                return

            self.window.fill((0, 0, 0))

            for platform in self.platform_list:
                if platform.state == -1 or platform.state == self.world_state:
                    self.window.blit(source=platform.surf, dest=platform.rect)

            self.window.blit(source=self.player.surf, dest=self.player.rect)

            pygame.display.flip()
