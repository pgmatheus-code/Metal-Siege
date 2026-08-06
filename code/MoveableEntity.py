from abc import ABC, abstractmethod
from code.Entity import Entity

class MoveableEntity(Entity, ABC):
    def __init__(self, entity_type: str, name: str, position: tuple, health: int, score: int, speed: int):
        Entity.__init__(self, entity_type, name, position, health, score)
        self.speed = speed


    @abstractmethod
    def move(self):
        pass