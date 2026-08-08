import sys

import pygame
from pygame import Surface, Rect

from code.Block import Block
from code.Const import SHADOW_DIRECTION, SHADOW_COLOR, FONT_MAIN, C_WHITE, WINDOW_SIZE, MAP_BOTTOMRIGHT, \
    MAP_TOPLEFT, LEVEL_FPS, STAGE_END_EVENT, STAGE_END_CHECK_INTERVAL, TIMEOUT_STEP, ENEMY_AMOUNT, ENEMY_AT_ONCE, \
    ENEMY_SPAWN_EVENT, C_RED
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
        self.check_endgame_timer = STAGE_END_CHECK_INTERVAL

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
        self.enemy_lives = ENEMY_AMOUNT
        self.entity_list: list[Entity] = []
        self.particle_group = pygame.sprite.Group()

        # player 1 instantiation
        player = EntityFactory.get_entity('player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode == 'TWO PLAYERS':
            # player 2 instantiation
            player = EntityFactory.get_entity('player2')
            player.score = player_score[0]
            self.entity_list.append(player)

        # map blocks instantiation
        self.entity_list.extend(EntityFactory.get_entity(name))

        pygame.time.set_timer(ENEMY_SPAWN_EVENT, TIMEOUT_STEP)

    def run(self, player_score):
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

            # generic hud ---------------------------------------------------
            self.window.blit(source=self.hud_background, dest=self.hud_rect)
            self.window.blit(source=self.map_background, dest=self.map_rect)

            # enemy_lives ---------------------------------------------------
            self.level_text(
                font_path=FONT_MAIN,
                text_size=25,
                text='Enemies',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                          MAP_TOPLEFT[1] + 10)
            )
            self.level_text(
                font_path=FONT_MAIN,
                text_size=25,
                text='left',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                          MAP_TOPLEFT[1] + 25)
            )
            enemy_text = self.get_enemy_lives_text(self.enemy_lives)
            self.level_break_line_text(
                font_path=FONT_MAIN,
                text_size=30,
                text=enemy_text,
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                          MAP_TOPLEFT[1] + 45)
            )

            # players hud -----------------------------------------------------------------
            self.level_text(  # PLAYER 1
                font_path=FONT_MAIN,
                text_size=30,
                text='P1',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                          MAP_TOPLEFT[1] + 230)
            )
            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text=self.player1_lives * 'I',
                text_color=C_WHITE,
                text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                          MAP_TOPLEFT[1] + 250)
            )

            self.level_text(
                font_path=FONT_MAIN,
                text_size=30,
                text='P1 SCORE: ',
                text_color=C_WHITE,
                text_pos=(100,
                          12)
            )
            for player in self.entity_list:
                if isinstance(player, Player) and player.name == 'player1':
                    self.level_text(
                        font_path=FONT_MAIN,
                        text_size=30,
                        text=f'{player.score:05d}',
                        text_color=C_WHITE,
                        text_pos=(210,
                                  12)
                    )

            if self.game_mode == 'TWO PLAYERS':
                self.level_text(  # PLAYER 2
                    font_path=FONT_MAIN,
                    text_size=30,
                    text='P2',
                    text_color=C_WHITE,
                    text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                              MAP_TOPLEFT[1] + 320)
                )
                self.level_text(
                    font_path=FONT_MAIN,
                    text_size=30,
                    text=self.player2_lives * 'I',
                    text_color=C_WHITE,
                    text_pos=(MAP_BOTTOMRIGHT[0] + ((WINDOW_SIZE[0] - MAP_BOTTOMRIGHT[0]) / 2),
                              MAP_TOPLEFT[1] + 340)
                )
                self.level_text(
                    font_path=FONT_MAIN,
                    text_size=30,
                    text='P2 SCORE: ',
                    text_color=C_WHITE,
                    text_pos=(WINDOW_SIZE[0] / 2 + 20,
                              12)
                )
                for player in self.entity_list:
                    if isinstance(player, Player) and player.name == 'player2':
                        self.level_text(
                            font_path=FONT_MAIN,
                            text_size=30,
                            text=f'{player.score:05d}',
                            text_color=C_WHITE,
                            text_pos=(WINDOW_SIZE[0] / 2 + 130,
                                      12)
                        )

            # draw explosions
            self.particle_group.update()
            self.particle_group.draw(self.window)

            # move and shot
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

            # player detection
            found_player1 = False
            found_player2 = False

            for moveable_search in self.entity_list:
                if not isinstance(moveable_search, MoveableEntity):
                    continue
                if isinstance(moveable_search, Player) and moveable_search.name == 'player1':
                    found_player1 = True
                if isinstance(moveable_search, Player) and moveable_search.name == 'player2':
                    found_player2 = True

            # resurrection
            if not found_player1 and self.player1_lives > 0:  # player 1
                self.player1_lives -= 1
                # player 1 resurrection
                player = EntityFactory.get_entity('player1')
                # player.score = player_score[0]
                self.entity_list.append(player)

            if self.game_mode == 'TWO PLAYERS':
                if not found_player2 and self.player2_lives > 0:  # player 2
                    self.player2_lives -= 1
                    # player 2 resurrection
                    player = EntityFactory.get_entity('player2')
                    # player.score = player_score[0]
                    self.entity_list.append(player)

            # flag detection
            found_flag = False
            for flag_search in self.entity_list:
                if isinstance(flag_search, Block) and flag_search.name == 'flag':
                    found_flag = True

            # loss condition
            if (not found_player2 and not found_player1) or not found_flag:
                self.game_over = True
                pygame.time.set_timer(STAGE_END_EVENT, TIMEOUT_STEP)
            else:
                self.game_over = False
                pygame.time.set_timer(STAGE_END_EVENT, 0)

            # get any pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ENEMY_SPAWN_EVENT:
                    current_enemy_amount = 0

                    for moveable_search in self.entity_list:
                        if isinstance(moveable_search, Enemy):
                            current_enemy_amount += 1

                    if current_enemy_amount < ENEMY_AT_ONCE:
                        if self.enemy_lives > 0:
                            self.enemy_lives -= 1
                            # enemy resurrection
                            enemy = EntityFactory.get_entity('enemy')
                            # player.score = player_score[0]
                            self.entity_list.append(enemy)
                    if current_enemy_amount == 0 and self.enemy_lives == 0:
                        pygame.time.set_timer(STAGE_END_EVENT, TIMEOUT_STEP)

                if event.type == STAGE_END_EVENT:

                    if self.check_endgame_timer > 0:
                        # subtract time from timeout
                        self.check_endgame_timer -= TIMEOUT_STEP
                    else:
                        # pass score
                        for entity in self.entity_list:
                            if isinstance(entity, Player) and entity.name == 'player1':
                                player_score[0] = entity.score
                            elif isinstance(entity, Player) and entity.name == 'player2':
                                player_score[1] = entity.score

                        # jump to the next stage or end game
                        pygame.time.set_timer(STAGE_END_EVENT, 0)
                        return not self.game_over

            # GAME OVER text
            if self.game_over and self.check_endgame_timer < STAGE_END_CHECK_INTERVAL * (7/8):

                timeout_value = self.check_endgame_timer - 1000 if self.check_endgame_timer > 1000 else 0
                pos_x = MAP_BOTTOMRIGHT[0] / 2
                pos_y = MAP_BOTTOMRIGHT[1] / 2 + timeout_value

                self.level_text(
                    font_path=FONT_MAIN,
                    text_size=70,
                    text='GAME',
                    text_color=C_RED,
                    text_pos=(pos_x, pos_y - 20)
                )
                self.level_text(
                    font_path=FONT_MAIN,
                    text_size=70,
                    text='OVER',
                    text_color=C_RED,
                    text_pos=(pos_x, pos_y + 20)
                )

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

    def get_enemy_lives_text(self, enemy_lives: int) -> str:
        # Build a string with enemy_lives copies of "I"
        lives_string = "I" * enemy_lives

        # Break into chunks of 5
        lines = [lives_string[i:i + 5] for i in range(0, len(lives_string), 5)]

        # Join with newline so your text renderer breaks lines
        return "\n".join(lines)

    def level_break_line_text(self, font_path: str, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: pygame.font.Font = pygame.font.Font(font_path, text_size)

        lines = text.split("\n")
        line_height = text_font.get_linesize()

        for i, line in enumerate(lines):
            y = text_pos[1] + i * line_height

            # shadow
            shadow_surface = text_font.render(line, True, SHADOW_COLOR).convert_alpha()
            shadow_rect = shadow_surface.get_rect(
                center=(text_pos[0] + SHADOW_DIRECTION[0], y + SHADOW_DIRECTION[1])
            )
            self.window.blit(shadow_surface, shadow_rect)

            # main
            text_surface = text_font.render(line, True, text_color).convert_alpha()
            text_rect = text_surface.get_rect(center=(text_pos[0], y))
            self.window.blit(text_surface, text_rect)
