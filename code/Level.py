import sys

import pygame
from pygame import Surface, Rect

from code.Const import SHADOW_DIRECTION, SHADOW_COLOR, FONT_MAIN, C_WHITE, WINDOW_SIZE, MAP_BOTTOMRIGHT, \
    MAP_TOPLEFT, LEVEL_FPS
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        # attributes
        self.player_score = player_score
        self.window = window
        self.name = name
        self.game_mode = game_mode

        # hud background
        self.hud_background = pygame.image.load('./assets/sprites/main_menu/main_menu_background.png').convert_alpha()
        self.hud_background = pygame.transform.scale(self.hud_background, self.window.get_size())
        self.hud_rect = self.hud_background.get_rect(topleft=(0, 0))

        # map background
        self.map_background = pygame.image.load('./assets/sprites/main_menu/map_background.png').convert_alpha()
        self.map_rect = self.map_background.get_rect(topleft=MAP_TOPLEFT)
        self.map_background = pygame.transform.scale(self.map_background, MAP_BOTTOMRIGHT)

        # spawning
        self.entity_list: list[Entity] = []

        # level blocks instantiation
        # self.entity_list.extend(EntityFactory.get_entity(name))

        # player 1 instantiation
        player = EntityFactory.get_entity('player1')
        # player.score = player_score[0]
        self.entity_list.append(player)

        # player 2 instantiation
        player = EntityFactory.get_entity('player2')
        # player.score = player_score[0]
        self.entity_list.append(player)

    def run(self):
        # Initialize mixer
        # pygame.mixer.init()

        # music
        # pygame.mixer.music.load(f'./assets/sounds/{self.name}.mp3')
        # pygame.mixer.music.play(-1)  # minus one for loop

        # clock
        clock = pygame.time.Clock()

        # main loop
        while True:
            clock.tick(LEVEL_FPS)

            # generic hud
            self.window.blit(source=self.hud_background, dest=self.hud_rect)
            self.window.blit(source=self.map_background, dest=self.map_rect)
            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text='P1',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15,
                          WINDOW_SIZE[1] / 2 - 40)
            )
            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text='P2',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15,
                          WINDOW_SIZE[1] / 2 + 40)
            )

            # entity specific
            for entity in self.entity_list:
                # apply drawing
                self.window.blit(source=entity.surf, dest=entity.rect)

                # move each stuff
                entity.move()

                # shot
                if isinstance(entity, (Player)):
                    shot = entity.shoot()
                    if shot is not None:
                        self.entity_list.append(shot)
                #
                #         entity_formatted_name = ''
                #
                #         if entity.name in ['player1_ship', 'player2_ship']:
                #             entity_formatted_name = entity.name[:-5]
                #         elif entity.name[:3] == 'foe':
                #             entity_formatted_name = 'foe'
                #
                #         if entity_formatted_name != '':
                #             shoot_sfx = pygame.mixer.Sound(f'./assets/sounds/{entity_formatted_name}_shot.mp3')
                #             shoot_sfx.set_volume(0.4)
                #             shoot_sfx.play()

                # player hud
                # if entity.name == 'player1_ship':
                #     self.level_text(
                #         text_size=14,
                #         text=f'Player 1 Health: {entity.health}',
                #         text_color=NEON_PINK,
                #         text_pos=(10, WIN_HEIGHT - 60)
                #     )
                #     self.level_text(
                #         text_size=14,
                #         text=f'Score: {entity.score}',
                #         text_color=NEON_PINK,
                #         text_pos=(10, WIN_HEIGHT - 30)
                #     )
                # if entity.name == 'player2_ship':
                #     self.level_text(
                #         text_size=14,
                #         text=f'Player 2 Health: {entity.health}',
                #         text_color=NEON_PINK,
                #         text_pos=(WIN_WIDTH - 230, WIN_HEIGHT - 60)
                #     )
                #     self.level_text(
                #         text_size=14,
                #         text=f'Score: {entity.score} PTS',
                #         text_color=NEON_PINK,
                #         text_pos=(WIN_WIDTH - 230, WIN_HEIGHT - 30)
                #     )

            # get any pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # standard quit event (to avoid window freeze)
                    pygame.quit()
                    sys.exit()

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