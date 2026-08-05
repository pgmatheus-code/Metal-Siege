from code.Const import SHOT_SPEED, SHOT_DAMAGE
from code.MoveableEntity import MoveableEntity

class Shot(MoveableEntity):
    def __init__(self, shooter: str, position: tuple, direction: tuple):
        MoveableEntity.__init__(
            self,
            entity_type='projectile',
            name =f'shot_projectile',
            position=position,
            health=1,
            score=0,
            speed=SHOT_SPEED,
            damage=SHOT_DAMAGE
        )

        print(f'{shooter} shot at {position}')

        self.shooter = shooter
        self.direction = direction

    def move(self):
        self.rect.centerx += self.direction[0] * SHOT_SPEED
        self.rect.centery += self.direction[1] * SHOT_SPEED