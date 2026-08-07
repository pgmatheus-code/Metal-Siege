#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import pygame.image
from pygame import Rect, Surface, KEYDOWN
from pygame.font import Font

from code.Const import LOGO_SIZE, WINDOW_SIZE, SHADOW_DIRECTION, SHADOW_COLOR, SIGN_SIZE, C_BLACK, \
    FONT_MAIN, TITLE_SIZE, MENU_OPTION, C_WHITE, MENU_HEIGHT, MENU_SPACING, MENU_OPTION_SIZE


class Menu:
    def __init__(self, window):
        self.window = window

        # background
        self.background = pygame.image.load('./assets/sprites/main_menu/main_menu_background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, self.window.get_size())
        self.rect = self.background.get_rect(topleft=(0, 0))


    def run(self, ):
        selected_option = 0

        # music
        # pygame.mixer.music.load('./assets/sounds/main_menu.mp3')
        # pygame.mixer.music.play(-1)  # minus one for loop

        while True:
            # DRAW -----------------------------------------------------------------------------------------------------
            # image
            self.window.blit(source=self.background, dest=self.rect)

            # title
            self.menu_text(
                font_path=FONT_MAIN,
                text_size=TITLE_SIZE,
                text=f'METAL',
                text_color=C_BLACK,
                text_pos=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 7)
            )
            self.menu_text(
                font_path=FONT_MAIN,
                text_size=TITLE_SIZE,
                text=f'SIEGE',
                text_color=C_BLACK,
                text_pos=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 3)
            )

            # sign
            self.menu_text(
                font_path=FONT_MAIN,
                text_size=SIGN_SIZE,
                text='This project is a student work inspired by Battle City (Namcot, 1985) ',
                text_color=C_WHITE,
                text_pos=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] - SIGN_SIZE / 2 - 15)
            )
            self.menu_text(
                font_path=FONT_MAIN,
                text_size=SIGN_SIZE,
                text='All trademarks and copyrights belong to their respective owners.',
                text_color=C_WHITE,
                text_pos=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] - SIGN_SIZE / 2)
            )

            # top hud
            self.menu_text(
                font_path=FONT_MAIN,
                text_size=SIGN_SIZE + 10,
                text='I-     00     HI-  20000',
                text_color=C_WHITE,
                text_pos=(200, SIGN_SIZE / 2)
            )

            # main menu
            for i in range(len(MENU_OPTION)):
                menu_opt_str = MENU_OPTION[i]

                if i == selected_option:
                    color = C_WHITE
                else:
                    color = C_BLACK

                # menu opt pos
                menu_opt_x = (WINDOW_SIZE[0] / 2)
                menu_opt_y = (MENU_HEIGHT + MENU_SPACING * i)

                # color main
                self.menu_text(
                    font_path=FONT_MAIN,
                    text_size=MENU_OPTION_SIZE,
                    text=menu_opt_str,
                    text_color=color,
                    text_pos=(menu_opt_x, menu_opt_y)
                )

            # update display
            pygame.display.flip()

            # EVENTS ---------------------------------------------------------------------------------------------------
            # checking all events
            for event in pygame.event.get():
                # quit events
                if event.type == pygame.QUIT:
                    pygame.quit()  # end pygame
                    sys.exit()  # close window

                selection_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/hud_selection.wav')
                selection_sfx.set_volume(0.4)

                if event.type == KEYDOWN:
                    # directional events
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if selected_option > 0:
                            selected_option -= 1
                        else:
                            selected_option = len(MENU_OPTION) - 1
                        selection_sfx.play()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if selected_option < len(MENU_OPTION) - 1:
                            selected_option += 1
                        else:
                            selected_option = 0
                        selection_sfx.play()

                    # enter events
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return MENU_OPTION[selected_option]

    def menu_text(self, font_path: str, text_size: int, text: str, text_color: tuple, text_pos: tuple):
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
