import random

from code.Block import Block
from code.Const import WINDOW_SIZE, MAP_TOPLEFT, MAP_BOTTOMRIGHT, MAP_SIZE, MAP_STAGE1, BLOCK_REF
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:
            case 'stage1':
                block_map = MAP_STAGE1
                return generate_block_list(block_map)
            case 'player1':
                return Player(player_name='player1', position=(MAP_BOTTOMRIGHT[0] / 2 - 65, MAP_BOTTOMRIGHT[1] - 30))
            case 'player2':
                return Player(player_name='player2', position=(MAP_BOTTOMRIGHT[0] / 2 + 65, MAP_BOTTOMRIGHT[1] - 30))
            case 'enemy':
                random_enemy = random.choice(['enemy1', 'enemy2', 'enemy3'])
                random_pos = random.choice([(MAP_TOPLEFT[0], MAP_TOPLEFT[1]), (MAP_BOTTOMRIGHT[0] - 32, MAP_TOPLEFT[0])])
                return Enemy(name= random_enemy, position= random_pos)
        return None

def generate_block_list(block_map: list[int]):
    block_list = []
    width = MAP_SIZE[0]
    height = MAP_SIZE[1]

    for i in range(width):
        for j in range(height):
            block_id = block_map[j * width + i]

            block_name = BLOCK_REF[block_id][0]
            is_solid = BLOCK_REF[block_id][1]
            is_shootable = BLOCK_REF[block_id][2]
            is_damageable = BLOCK_REF[block_id][3]

            block_size = 32
            pos_x = i * block_size
            pos_y = j * block_size
            position = (MAP_TOPLEFT[0] + pos_x, MAP_TOPLEFT[1] + pos_y)

            if block_name != 'none':
                block_list.append(
                    Block(
                        name=f'{block_name}',
                        position=position,
                        health=100,
                        score=50,
                        is_solid= is_solid,
                        is_shootable= is_shootable,
                        is_damageable= is_damageable
                    )
                )

    return block_list