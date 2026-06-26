import sys

import pygame
from pygame import Surface

from code.Const import COLLISION_MAP_LEVEL1_0, COLLISION_MAP_LEVEL1_1
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

            # current collision map
            if self.world_state == 0:
                collision_map = COLLISION_MAP_LEVEL1_0
            else:
                collision_map = COLLISION_MAP_LEVEL1_1

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

            # player update
            keys = pygame.key.get_pressed()

            self.player.update(keys, collision_map)

            # player fell
            if self.player.rect.top > self.window.get_height():
                return

            # draw
            for platform in self.platform_list:
                if platform.state == -1 or platform.state == self.world_state:
                    self.window.blit(source=platform.surf, dest=platform.rect)

            self.window.blit(source=self.player.surf, dest=self.player.rect)
            pygame.display.flip()
