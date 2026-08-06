import random

import pygame

from code.Const import PLAYER_SHOT_DELAY, KEY_LEFT, PLAYER_SPEED, KEY_RIGHT, KEY_UP, \
    KEY_DOWN, KEY_SHOOT, MAP_TOPLEFT, MAP_BOTTOMRIGHT, ENEMY_SHOT_DELAY, ENEMY_HEALTH, ENEMY_SPEED, \
    ENEMY_RANDOM_MOVEMENT_DELAY
from code.MoveableEntity import MoveableEntity
from code.Shot import Shot


class Enemy(MoveableEntity):
    def __init__(self, name: str, position: tuple):
        MoveableEntity.__init__(
            self,
            entity_type='tank',
            name=name,
            position=position,
            health=ENEMY_HEALTH[name],
            score=0,
            speed=ENEMY_SPEED[name]
        )

        self.damage = 1
        self.movement_timer = 0
        self.is_movement_ready = False
        self.shot_timer = ENEMY_SHOT_DELAY[name]
        self.is_shot_ready = False

        self.random_direction = ''
        self.random_movement_timer = ENEMY_RANDOM_MOVEMENT_DELAY[name]
        self.angle = 0
        self.original_image = self.surf


    def move(self):

        if self.random_movement_timer > 0:
            self.random_movement_timer -= 1
        else:
            self.random_movement_timer = ENEMY_RANDOM_MOVEMENT_DELAY[self.name] * random.randint(5, 10)
            self.random_direction = random.choice(['up', 'down', 'left', 'right', ''])

        moved = False
        if self.movement_timer > 0:
            self.movement_timer -= self.speed
            return

        speed = 5

        if self.random_direction == 'left' and self.rect.left > MAP_TOPLEFT[0]:
            self.dx = -speed
            self.angle = 90
            moved = True
        elif self.random_direction == 'right' and self.rect.right < MAP_BOTTOMRIGHT[0]:
            self.dx = +speed
            self.angle = 270
            moved = True
        elif self.random_direction == 'up' and self.rect.top > MAP_TOPLEFT[1]:
            self.dy = -speed
            self.angle = 0
            moved = True
        elif self.random_direction == 'down' and self.rect.bottom < MAP_BOTTOMRIGHT[1]:
            self.dy = +speed
            self.angle = 180
            moved = True

        # apply rotation
        if moved:
            self.movement_timer = 60
            self.surf = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.surf.get_rect(center=self.rect.center)

    def shoot(self):
        # direction angle based { angle, direction
        direction_dict = {
            0: (0, -1),
            90: (-1, 0),
            180: (0, 1),
            270: (1, 0),
        }

        if self.shot_timer > 0:
            self.shot_timer -= 1
        else:
            self.shot_timer = ENEMY_SHOT_DELAY[self.name] * random.randint(1, 5)
            return Shot(
                shooter=self.name,
                position=(self.rect.centerx, self.rect.centery),
                direction=direction_dict[self.angle]
            )
        return None
