from abc import ABC

from code.Entity import Entity


class Block(Entity):
    def __init__(self, name: str, position: tuple, health: int, score: int, is_solid: bool, is_destructible: bool):
        Entity.__init__(
            self,
            entity_type='block',
            name= name,
            position= position,
            health= health,
            score= score
        )

        self.is_solid = is_solid # by tanks
        self.is_destructible = is_destructible # by shots
