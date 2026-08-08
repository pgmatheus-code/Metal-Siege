import random

from code.Block import Block
from code.Const import WINDOW_SIZE, MAP_TOPLEFT, MAP_BOTTOMRIGHT, MAP_SIZE, MAP_UNINTER, BLOCK_REF, MAP_ORIGINAL, \
    MAP_ARENA, MAP_MAZE
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:
    last_enemy_spawn_pos_index = 0

    @staticmethod
    def get_entity(entity_name: str):

        match entity_name:
            case 'stage1':
                block_map = MAP_UNINTER
                return generate_block_list(block_map)
            case 'stage2':
                block_map = MAP_ORIGINAL
                return generate_block_list(block_map)
            case 'stage3':
                block_map = MAP_ARENA
                return generate_block_list(block_map)
            case 'stage4':
                block_map = MAP_MAZE
                return generate_block_list(block_map)
            case 'player1':
                return Player(player_name='player1', position=(MAP_BOTTOMRIGHT[0] / 2 - 65, MAP_BOTTOMRIGHT[1] - 30))
            case 'player2':
                return Player(player_name='player2', position=(MAP_BOTTOMRIGHT[0] / 2 + 65, MAP_BOTTOMRIGHT[1] - 30))
            case 'enemy':
                random_enemy = random.choice(['enemy1', 'enemy2', 'enemy3'])
                spawn_pos = [
                    (MAP_TOPLEFT[0], MAP_TOPLEFT[1]),               #top_left
                    (MAP_BOTTOMRIGHT[0] / 2 - 32, MAP_TOPLEFT[1]),  #top_center
                    (MAP_BOTTOMRIGHT[0] - 32, MAP_TOPLEFT[1])       #top_right
                ]
                if EntityFactory.last_enemy_spawn_pos_index < len(spawn_pos) - 1:
                    EntityFactory.last_enemy_spawn_pos_index += 1
                else:
                    EntityFactory.last_enemy_spawn_pos_index = 0

                pos_index = EntityFactory.last_enemy_spawn_pos_index
                return Enemy(name= random_enemy, position= spawn_pos[pos_index])
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
            score = BLOCK_REF[block_id][4]

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
                        score=score,
                        is_solid= is_solid,
                        is_shootable= is_shootable,
                        is_damageable= is_damageable
                    )
                )

    return block_list