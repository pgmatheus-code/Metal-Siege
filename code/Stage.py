import sys

import pygame
from pygame import Surface, Rect

from code.Block import Block
from code.Const import SHADOW_DIRECTION, SHADOW_COLOR, FONT_MAIN, C_WHITE, WINDOW_SIZE, MAP_BOTTOMRIGHT, \
    MAP_TOPLEFT, LEVEL_FPS
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.MoveableEntity import MoveableEntity
from code.Player import Player
from code.Shot import Shot


class Stage:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        # attributes
        self.player_score = player_score
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.game_over = False

        # hud background
        self.hud_background = pygame.image.load('./assets/sprites/main_menu/main_menu_background.png').convert_alpha()
        self.hud_background = pygame.transform.scale(self.hud_background, self.window.get_size())
        self.hud_rect = self.hud_background.get_rect(topleft=(0, 0))

        # map background
        self.map_background = pygame.image.load('./assets/sprites/main_menu/map_background.png').convert_alpha()
        self.map_rect = self.map_background.get_rect(topleft=MAP_TOPLEFT)
        scale_tuple = ((MAP_BOTTOMRIGHT[0] - MAP_TOPLEFT[0]), (MAP_BOTTOMRIGHT[1] - MAP_TOPLEFT[1]))
        self.map_background = pygame.transform.scale(self.map_background, scale_tuple)

        # spawning
        self.player1_lives = 3
        self.player2_lives = 3
        self.entity_list: list[Entity] = []
        self.particle_group = pygame.sprite.Group()

        # player 1 instantiation
        player = EntityFactory.get_entity('player1')
        # player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode == 'TWO PLAYERS':
            # player 2 instantiation
            player = EntityFactory.get_entity('player2')
            # player.score = player_score[0]
            self.entity_list.append(player)

        # example enemy instantiation
        for i in range(2):
            enemy = EntityFactory.get_entity('enemy')
            self.entity_list.append(enemy)

        # map blocks instantiation
        self.entity_list.extend(EntityFactory.get_entity(name))

    def run(self):
        # Initialize mixer
        pygame.mixer.init()

        # music
        pygame.mixer.music.load(f'./assets/sounds/game_start_theme.mp3')
        pygame.mixer.music.play()  # minus one for loop

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
            if self.game_mode == 'TWO PLAYERS':
                self.level_text(
                    font_path=FONT_MAIN,
                    text_size=30,
                    text='P2',
                    text_color=C_WHITE,
                    text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15,
                              WINDOW_SIZE[1] / 2 + 40)
                )

            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text=self.player1_lives * 'I',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15,
                          WINDOW_SIZE[1] / 2 - 20)
            )

            if self.game_mode == 'TWO PLAYERS':
                self.level_text(
                    font_path=FONT_MAIN,
                    text_size=30,
                    text=self.player2_lives * 'I',
                    text_color=C_WHITE,
                    text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2) + 15,
                              WINDOW_SIZE[1] / 2 + 60)
                )

            # draw explosions
            self.particle_group.update()
            self.particle_group.draw(self.window)

            # entity specific
            for entity in self.entity_list:
                # apply drawing
                self.window.blit(source=entity.surf, dest=entity.rect)

                # move each stuff
                if isinstance(entity, MoveableEntity):
                    if not self.game_over or (self.game_over and not isinstance(entity, Player)):
                        entity.move()

                        if not isinstance(entity, Shot):
                            EntityMediator.check_collision_after_movement(entity, self.entity_list)

                # shot
                if isinstance(entity, (Player, Enemy)):
                    if not self.game_over or (self.game_over and not isinstance(entity, Player)):
                        shot = entity.shoot()
                        if shot is not None:
                            self.entity_list.append(shot)

                            if entity.name in ['player1', 'player2']:
                                shoot_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/tank_shot.wav')
                                shoot_sfx.set_volume(0.4)
                                shoot_sfx.play()

                found_player1 = False
                found_player2 = False
                for player_search in self.entity_list:
                    if isinstance(player_search, Player) and player_search.name == 'player1':
                        found_player1 = True
                    if isinstance(player_search, Player) and player_search.name == 'player2':
                        found_player2 = True

                # game over condition or resurrection
                if not found_player1 and self.player1_lives > 0:
                    self.player1_lives -= 1
                    # player 1 resurrection
                    player = EntityFactory.get_entity('player1')
                    # player.score = player_score[0]
                    self.entity_list.append(player)

                if self.game_mode == 'TWO PLAYERS':
                    if not found_player2 and self.player2_lives > 0:
                        self.player2_lives -= 1
                        # player 2 resurrection
                        player = EntityFactory.get_entity('player2')
                        # player.score = player_score[0]
                        self.entity_list.append(player)

                found_flag = False
                for flag_search in self.entity_list:
                    if isinstance(flag_search, Block) and flag_search.name == 'flag':
                        found_flag = True

                if (not found_player2 and not found_player1) or not found_flag:
                    self.game_over = True
                else:
                    self.game_over = False

            # get any pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # standard quit event (to avoid window freeze)
                    pygame.quit()
                    sys.exit()

            # update display
            pygame.display.flip()

            # Entity mediator - entity damage and destruction
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list, particle_group=self.particle_group)

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
