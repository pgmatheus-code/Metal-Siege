import pygame
from pygame import Surface, Rect

from code.Const import SHADOW_DIRECTION, SHADOW_COLOR, FONT_MAIN, C_WHITE, WINDOW_SIZE, MAP_BOTTOMRIGHT, \
    MAP_TOPLEFT


class Level:
    def __init__(self, window: Surface):
        self.window = window

        # hud background
        self.hud_background = pygame.image.load('./assets/sprites/main_menu/main_menu_background.png').convert_alpha()
        self.hud_background = pygame.transform.scale(self.hud_background, self.window.get_size())
        self.hud_rect = self.hud_background.get_rect(topleft=(0, 0))

        # map background
        self.map_background = pygame.image.load('./assets/sprites/main_menu/map_background.png').convert_alpha()
        self.map_rect = self.map_background.get_rect(topleft=MAP_TOPLEFT)
        self.map_background = pygame.transform.scale(self.map_background, MAP_BOTTOMRIGHT)

    def run(self):
        selected_option = 0

        # music
        # pygame.mixer.music.load('./assets/sounds/main_menu.mp3')
        # pygame.mixer.music.play(-1)  # minus one for loop

        while True:
            # DRAW -----------------------------------------------------------------------------------------------------
            # image
            self.window.blit(source=self.hud_background, dest=self.hud_rect)
            self.window.blit(source=self.map_background, dest=self.map_rect)

            # player hud labels
            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text='P1',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15, WINDOW_SIZE[1] / 2 - 40)
            )

            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text='P2',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15, WINDOW_SIZE[1] / 2 + 40)
            )

            # # main menu
            # for i in range(len(MENU_OPTION)):
            #     menu_opt_str = MENU_OPTION[i]
            #
            #     if i == selected_option:
            #         color = C_WHITE
            #     else:
            #         color = C_BLACK
            #
            #     # menu opt pos
            #     menu_opt_x = (WINDOW_SIZE[0] / 2)
            #     menu_opt_y = (MENU_HEIGHT + MENU_SPACING * i)
            #
            #     # color main
            #     self.menu_text(
            #         font_path=FONT_LARGEFONTS,
            #         text_size=MENU_OPTION_SIZE,
            #         text=menu_opt_str,
            #         text_color=color,
            #         text_pos=(menu_opt_x, menu_opt_y)
            #     )

            # update display
            pygame.display.flip()

    def level_text(self, font_path: str, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: pygame.font.Font = pygame.font.Font(font_path, text_size)

        # shadow
        text_shadow_surface: Surface = text_font.render(text, True, SHADOW_COLOR).convert_alpha()
        text_shadow_rect: Rect = text_shadow_surface.get_rect(
            center=(text_pos[0] + SHADOW_DIRECTION[0], text_pos[1] + SHADOW_DIRECTION[1]))
        self.window.blit(source=text_shadow_surface, dest=text_shadow_rect)

        # main
        text_surface: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surface.get_rect(center=text_pos)
        self.window.blit(source=text_surface, dest=text_rect)