import sys
import pygame
from pygame import Surface, Rect, KEYDOWN
from code.Const import SHADOW_DIRECTION, SHADOW_COLOR, MAP_BOTTOMRIGHT, MAP_TOPLEFT, WINDOW_SIZE


class Controls:
    def __init__(self, window: Surface):
        # attributes
        self.window = window

        # hud background
        self.background = pygame.image.load('./assets/sprites/main_menu/main_menu_background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, self.window.get_size())
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        # bindings png
        self.bindings_png = pygame.image.load('./assets/sprites/main_menu/key_bindings.png').convert_alpha()
        self.bindings_rect = self.bindings_png.get_rect(topleft=MAP_TOPLEFT)
        scale_tuple = ((WINDOW_SIZE[0] - MAP_TOPLEFT[0]*2), (MAP_BOTTOMRIGHT[1] - MAP_TOPLEFT[1]))
        self.bindings_png = pygame.transform.scale(self.bindings_png, scale_tuple)

    def show(self):
        # music
        selection_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/hud_selection.wav')
        selection_sfx.set_volume(0.4)
        self.window.blit(source=self.background, dest=self.background_rect)
        self.window.blit(source=self.bindings_png, dest=self.bindings_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # end pygame
                    sys.exit()  # close window
                elif event.type == KEYDOWN:
                        return

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
