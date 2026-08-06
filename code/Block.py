from abc import ABC

from code.Entity import Entity


class Block(Entity):
    def __init__(self, name: str, position: tuple, health: int, score: int, is_solid: bool, is_shootable: bool, is_damageable: bool):
        Entity.__init__(
            self,
            entity_type='block',
            name= name,
            position= position,
            health= health,
            score= score
        )
        self.damage = 1

        self.is_solid = is_solid # passed by tanks
        self.is_shootable = is_shootable # passed by shots
        self.is_damageable = is_damageable # loss health
