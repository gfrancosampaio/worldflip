import sys

import pygame
from pygame import Surface

from code.Const import COLLISION_MAP_LEVEL1_0, COLLISION_MAP_LEVEL1_1, PLAYER_SPAWN, COLLISION_MAPS, PORTAL_SPAWN, \
    KEY_JUMP
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
        portal_pos = PORTAL_SPAWN[self.name]
        next_level = f'Level{int(self.name[-1]) + 1}'
        self.player = Player('Player', spawn_pos)
        self.portal = EntityFactory.get_entity('Portal', portal_pos, next_level)
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
                    if event.key == KEY_JUMP:
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
                return 'DEAD'

            # portal hitbox (next level)
            if self.player.rect.colliderect(self.portal.rect):
                # end of game demonstration
                if self.name == 'Level2':
                    return 'END'
                # go to next level (only to level 2 in DEMO)
                return self.portal.next_level

            # draw
            for platform in self.platform_list:
                if platform.state == -1 or platform.state == self.world_state:
                    self.window.blit(source=platform.surf, dest=platform.rect)

            self.window.blit(source=self.player.surf, dest=self.player.rect)
            self.window.blit(source=self.portal.surf, dest=self.portal.rect)
            pygame.display.flip()
