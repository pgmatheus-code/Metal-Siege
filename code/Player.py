import pygame

from code.Const import PLAYER_HEALTH, PLAYER_SHOT_DELAY, KEY_LEFT, PLAYER_SPEED, KEY_RIGHT, KEY_UP, \
    KEY_DOWN, KEY_SHOOT, MAP_TOPLEFT, MAP_BOTTOMRIGHT
from code.MoveableEntity import MoveableEntity
from code.Shot import Shot


class Player(MoveableEntity):
    def __init__(self, player_name: str, position: tuple):
        MoveableEntity.__init__(
            self,
            entity_type='tank',
            name=player_name,
            position=position,
            health=PLAYER_HEALTH,
            score=0,
            speed=PLAYER_SPEED
        )

        self.damage = 1
        self.movement_timer = 0
        self.is_movement_ready = False
        self.shot_timer = PLAYER_SHOT_DELAY
        self.is_shot_ready = False
        self.angle = 0
        self.original_image = self.surf

    def move(self):
        pressed_key = pygame.key.get_pressed()
        player_name = self.name
        moved = False

        if self.movement_timer > 0:
            self.movement_timer -= PLAYER_SPEED
            return

        speed = 5

        if pressed_key[KEY_LEFT[player_name]] and self.rect.left > MAP_TOPLEFT[0]:
            self.dx = -speed
            self.angle = 90
            moved = True
        elif pressed_key[KEY_RIGHT[player_name]] and self.rect.right < MAP_BOTTOMRIGHT[0]:
            self.dx = speed
            self.angle = 270
            moved = True
        elif pressed_key[KEY_UP[player_name]] and self.rect.top > MAP_TOPLEFT[1]:
            self.dy = -speed
            self.angle = 0
            moved = True
        elif pressed_key[KEY_DOWN[player_name]] and self.rect.bottom < MAP_BOTTOMRIGHT[1]:
            self.dy = speed
            self.angle = 180
            moved = True
        else:
            self.dx = 0
            self.dy = 0
            moved = False

        # apply rotation
        if moved:
            self.movement_timer = 60
            self.surf = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.surf.get_rect(center=self.rect.center)

    def shoot(self):
        player_name = self.name
        pressed_key = pygame.key.get_pressed()

        if self.shot_timer > 0:
            self.shot_timer -= 1
        else:
            self.is_shot_ready = True

        if pressed_key[KEY_SHOOT[player_name]] and self.is_shot_ready:
            self.shot_timer = PLAYER_SHOT_DELAY
            self.is_shot_ready = False

            # direction angle based { angle, direction
            direction_dict = {
                0 :  (0, -1),
                90 : (-1, 0),
                180 : (0, 1),
                270 : (1, 0),
            }

            return Shot(
                shooter=player_name,
                position=(self.rect.centerx, self.rect.centery),
                direction=direction_dict[self.angle]
            )

        return None
