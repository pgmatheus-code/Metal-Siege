import pygame

from code.Const import PLAYER_HEALTH, PLAYER_DAMAGE, PLAYER_SHOT_DELAY, KEY_LEFT, PLAYER_SPEED, KEY_RIGHT, KEY_UP, \
    KEY_DOWN, WINDOW_SIZE, KEY_SHOOT
from code.MoveableEntity import MoveableEntity


class Player(MoveableEntity):
    def __init__(self, player_name: str, position: tuple):
        MoveableEntity.__init__(
            self,
            entity_type='tank',
            name=f'tank_{player_name}',
            position=position,
            health=PLAYER_HEALTH,
            score=0,
            speed=PLAYER_SPEED,
            damage=PLAYER_DAMAGE
        )
        print(f'{player_name} at {position}')

        self.shot_timer = PLAYER_SHOT_DELAY
        self.is_shot_ready = False

    def move(self):
        pressed_key = pygame.key.get_pressed()
        player_name = self.name[5:]

        if pressed_key[KEY_LEFT[player_name]] and self.rect.left > 10:
            self.rect.centerx -= PLAYER_SPEED
        if pressed_key[KEY_RIGHT[player_name]] and self.rect.right < WINDOW_SIZE[0] - 10:
            self.rect.centerx += PLAYER_SPEED
        if pressed_key[KEY_UP[player_name]] and self.rect.top > 10:
            self.rect.centery -= PLAYER_SPEED
        if pressed_key[KEY_DOWN[player_name]] and self.rect.bottom < WINDOW_SIZE[1] - 10:
            self.rect.centery += PLAYER_SPEED

    def shoot(self):

        player_name = self.name[:7]
        pressed_key = pygame.key.get_pressed()

        if self.shot_timer > 0:
            self.shot_timer -= 1
        else:
            self.is_shot_ready = True

        if pressed_key[KEY_SHOOT[player_name]] and self.is_shot_ready:
            self.shot_timer = PLAYER_SHOT_DELAY
            self.is_shot_ready = False

            return PlayerShot(name=f'{player_name}_shot', position=(self.rect.centerx, self.rect.centery))
        return None