from abc import ABC
import pygame

class Entity(ABC):
    def __init__(self, entity_type: str, name: str, position: tuple, health: int, score: int):
        self.name = name
        self.surf = pygame.image.load(f'./assets/sprites/{entity_type}/{name}.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.position = position
        self.health = health
        self.last_dmg = 'None'
        self.score = score