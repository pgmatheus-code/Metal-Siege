from code.Const import WINDOW_SIZE
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
                return Player(player_name='player1', position=(WINDOW_SIZE[0] / 2, (WINDOW_SIZE[1] / 2) - 15))
            # case 'player2':
            #     return Player(name='player2', position=(10, (WIN_HEIGHT / 2) + 15))
            # case 'foe':
            #     return Foe(name='foe', position=(WIN_WIDTH + 20, random.randint(10, WIN_HEIGHT - 50)))
        return None