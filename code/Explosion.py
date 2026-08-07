import pygame
from pygame.sprite import Sprite
from code.Const import EXPLOSION_FRAME_RATE

import pygame

class Explosion(Sprite):
    frames = []  # empty until loaded

    @classmethod
    def load_frames(cls):
        cls.frames = [
            pygame.image.load("./assets/sprites/particle/explosion_0.png").convert_alpha(),
            pygame.image.load("./assets/sprites/particle/explosion_1.png").convert_alpha(),
            pygame.image.load("./assets/sprites/particle/explosion_2.png").convert_alpha(),
            pygame.image.load("./assets/sprites/particle/explosion_3.png").convert_alpha(),
            pygame.image.load("./assets/sprites/particle/explosion_4.png").convert_alpha()
        ]

    def __init__(self, position):
        super().__init__()
        self.index = 0
        self.frame_rate = EXPLOSION_FRAME_RATE
        self.counter = 0
        self.image = Explosion.frames[self.index]
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.counter = 0
            self.index += 1
            if self.index >= len(Explosion.frames):
                self.kill()
            else:
                self.image = Explosion.frames[self.index]