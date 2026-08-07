import pygame

from code.Block import Block
from code.Const import WINDOW_SIZE, MAP_TOPLEFT, MAP_BOTTOMRIGHT, BLOCK_REF
from code.Enemy import Enemy
from code.Entity import Entity
from code.MoveableEntity import MoveableEntity
from code.Player import Player
from code.Shot import Shot


class EntityMediator:
    @staticmethod
    def check_collision_after_movement(entity: MoveableEntity, entity_list: list[Entity]):
        # First, attempt the move
        entity.rect.centerx += entity.dx
        entity.rect.centery += entity.dy

        collided = False
        for compared_entity in entity_list:
            if entity == compared_entity: continue
            if isinstance(entity, Shot) or isinstance(compared_entity, Shot): continue
            if (isinstance(compared_entity, Block) and not compared_entity.is_solid): continue
            if (isinstance(entity, Block) and not entity.is_solid): continue

            # Check overlap
            if (entity.rect.right >= compared_entity.rect.left and
                    entity.rect.left <= compared_entity.rect.right and
                    entity.rect.bottom >= compared_entity.rect.top and
                    entity.rect.top <= compared_entity.rect.bottom):
                collided = True
                print(f'collided with {compared_entity.name}')
                break  # stop checking once collision is found

        # If collided, revert
        if collided:
            entity.rect.centerx -= entity.dx
            entity.rect.centery -= entity.dy

        # Reset movement deltas
        entity.dx = 0
        entity.dy = 0


    @staticmethod
    def __verify_collision_window(entity: Entity):  # private out-of-bounds destruction
        if isinstance(entity, Shot):  # similar to if (entity is Enemy) from c#
            if (    entity.rect.left < MAP_TOPLEFT[0] or
                    entity.rect.right > MAP_BOTTOMRIGHT[0] or
                    entity.rect.top < MAP_TOPLEFT[1] or
                    entity.rect.bottom > MAP_BOTTOMRIGHT[1]
            ):
                entity.health = 0

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            EntityMediator.__verify_collision_window(entity=entity_list[i])

            for j in range(i + 1, len(entity_list)):
                EntityMediator.__verify_collision_entity(entity_list[i], entity_list[j])

    @staticmethod
    def __give_score(enemy: Entity, entity_list: list[Entity]):
        if enemy.last_dmg == 'player1_shot':
            for entity in entity_list:
                if entity.name == 'player1':
                    entity.score += enemy.score
        elif enemy.last_dmg == 'player2_shot':
            for entity in entity_list:
                if entity.name == 'player2':
                    entity.score += enemy.score

    @staticmethod
    def __verify_collision_entity(entity1: Entity, entity2: Entity):  # private

        # avoid friendly fire
        is_interaction_valid = False
        if (
                (isinstance(entity1, Player) and isinstance(entity2, Shot)) and entity2.shooter != entity1.name or
                (isinstance(entity1, Shot) and isinstance(entity2, Player)) and entity1.shooter != entity2.name or
                (isinstance(entity1, Enemy) and isinstance(entity2, Shot)) and entity2.shooter != entity1.name or
                (isinstance(entity1, Shot) and isinstance(entity2, Enemy)) and entity1.shooter != entity2.name or
                (isinstance(entity1, Block) and entity1.is_shootable and isinstance(entity2, Shot)) or
                (isinstance(entity1, Shot) and isinstance(entity2, Block))  and entity2.is_shootable
        ):
            is_interaction_valid = True

        if is_interaction_valid:
            if (entity1.rect.right >= entity2.rect.left and
                    entity1.rect.left <= entity2.rect.right and
                    entity1.rect.bottom >= entity2.rect.top and
                    entity1.rect.top <= entity2.rect.bottom
            ):
                # entity2 damages entity1
                if not isinstance(entity1, Block) or isinstance(entity1, Block) and entity1.is_damageable:
                    entity1.last_dmg = entity2.name
                    entity1.health -= entity2.damage

                # entity1 damages entity2
                if not isinstance(entity2, Block) or isinstance(entity2, Block) and entity2.is_damageable:
                    entity2.last_dmg = entity1.name
                    entity2.health -= entity1.damage

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for entity in entity_list:
            if entity.health > 0: continue

            if isinstance(entity, Enemy):
                EntityMediator.__give_score(entity, entity_list)

            if isinstance(entity, Player):
                explosion_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/player_explosion.wav')
                explosion_sfx.set_volume(0.4)
                explosion_sfx.play()
            elif isinstance(entity, Enemy):
                explosion_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/enemy_explosion.wav')
                explosion_sfx.set_volume(0.4)
                explosion_sfx.play()
            elif isinstance(entity, Shot) and entity.shooter.startswith('player'):
                explosion_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/shot_collision.wav')
                explosion_sfx.set_volume(0.4)
                explosion_sfx.play()
            elif isinstance(entity, Block) and entity.name == 'flag':
                explosion_sfx = pygame.mixer.Sound(f'./assets/sounds/sfx/flag_destruction.wav')
                explosion_sfx.set_volume(4)
                explosion_sfx.play()

                entity_list.append(Block(
                    name=BLOCK_REF[4][0], # 'flag_destroyed'
                    position= entity.position,
                    health=100,
                    score=entity.score,
                    is_solid=BLOCK_REF[4][1],
                    is_shootable=BLOCK_REF[4][2],
                    is_damageable=BLOCK_REF[4][3],
                ))

            entity_list.remove(entity)