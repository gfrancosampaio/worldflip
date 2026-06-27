import sys

import pygame
from pygame import Surface

from code.Const import COLLISION_MAP_LEVEL1_0, COLLISION_MAP_LEVEL1_1, PLAYER_SPAWN, COLLISION_MAPS
from code.EntityFactory import EntityFactory
from code.Platform import Platform
from code.Player import Player
from code.Portal import Portal


class Level:
    def __init__(self, window: Surface, name: str):
        self.window = window
        self.name = name
        self.collision_maps = COLLISION_MAPS[self.name]
        self.world_state = 0
        spawn_pos = PLAYER_SPAWN[self.name]
        self.player = Player('Player', spawn_pos)
        self.portal = Portal('Portal1', (755, 60), f'Level{int(self.name[-1]) + 1}')
        self.platform_list: list[Platform] = []
        self.platform_list.extend(EntityFactory.get_entity(self.name + 'Plat'))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            # current collision map
            collision_map = self.collision_maps[self.world_state]

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

                    if event.key == pygame.K_ESCAPE:
                        return

            # player update
            keys = pygame.key.get_pressed()

            self.player.update(keys, collision_map)

            # player fell
            if self.player.rect.top > self.window.get_height():
                return

            # portal hitbox (next level)
            if self.player.rect.colliderect(self.portal.rect):
                return f'Level{int(self.name[-1]) + 1}'

            # draw
            for platform in self.platform_list:
                if platform.state == -1 or platform.state == self.world_state:
                    self.window.blit(source=platform.surf, dest=platform.rect)

            self.window.blit(source=self.player.surf, dest=self.player.rect)
            self.window.blit(source=self.portal.surf, dest=self.portal.rect)
            pygame.display.flip()
