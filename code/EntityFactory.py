import random

from code.Const import WINDOW_SIZE, MAP_TOPLEFT, MAP_BOTTOMRIGHT
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:
            # case 'city1' | 'city2' | 'city3' | 'city4':
            #     list_bg = []
            #     for i in range(8):
            #         list_bg.append(Background(name=f'{entity_name}/layer{i + 1}', position=(0, 0)))
            #         list_bg.append(Background(name=f'{entity_name}/layer{i + 1}', position=(WIN_WIDTH, 0)))
            #     return list_bg
            case 'player1':
                return Player(player_name='player1', position=(MAP_BOTTOMRIGHT[0] / 2 - 15, MAP_BOTTOMRIGHT[1] - 30))
            case 'player2':
                return Player(player_name='player2', position=(MAP_BOTTOMRIGHT[0] / 2 + 15, MAP_BOTTOMRIGHT[1] - 30))
            case 'enemy':
                random_pos = (random.randint(MAP_TOPLEFT[0], MAP_BOTTOMRIGHT[0]), random.randint(MAP_TOPLEFT[1], MAP_BOTTOMRIGHT[1]))
                return Enemy(name='foe', position=random_pos)
        return None