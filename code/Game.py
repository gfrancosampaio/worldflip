import sys

import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.level_index = 1

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            # play option
            if menu_return == MENU_OPTION[0]:
                self.level_index = 1

                while True:
                    level_name = f'Level{self.level_index}'

                    # intro screen (2 seconds)
                    self.show_level_intro(f'./asset/{level_name}.png')

                    # level start
                    level = Level(self.window, level_name)
                    result = level.run()

                    # next level
                    if result is None:
                        break
                    level_name = result
                    self.level_index = int(level_name [-1])

            # exit option
            elif menu_return == MENU_OPTION[1]:
                pygame.quit()
                quit()

            else:
                pygame.quit()
                sys.exit()

    def show_level_intro(self, image_path):
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (self.window.get_width(), self.window.get_height()))
        self.rect = self.surf.get_rect(left=0, top=0)
        start_time = pygame.time.get_ticks()

        while True:
            self.window.blit(self.surf, self.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if pygame.time.get_ticks() - start_time >= 2000:
                return
