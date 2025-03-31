import pygame
from code import level
from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Explosion import Explosion
from code.Player import Player
from code.PlayerShot import PlayerShot

class EntityMediator:
    enemy_passed_count = 0  # Contador de inimigos que saíram da tela
    enemy_limit = 1  # Número limite de inimigos que podem passar antes de perder

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:  # O inimigo saiu da tela
                ent.health = 0  # Define a saúde para 0
                ent.last_dmg = "Saída da tela"  # Marca que a destruição foi por saída da tela
                EntityMediator.enemy_passed_count += 1  # Aumenta o contador de inimigos que passaram

                # Verifica se o limite de inimigos que passaram foi alcançado
                if EntityMediator.enemy_passed_count >= EntityMediator.enemy_limit:
                    return True  # Retorna True quando o número de inimigos que saíram atinge o limite

        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0

        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

        return False


    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            if EntityMediator.__verify_collision_window(entity1):
                return True  # Retorna True quando o game over ocorre (condição de derrota atingida)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

        return False  # Retorna False se não houver game over


    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                # Aplica o dano nas duas entidades
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

                # Se o ent1 for um inimigo, aplica o dano ao inimigo
                if isinstance(ent1, Player):
                    ent1.apply_damage(ent2.damage)

                # Se o ent2 for um jogador, aplica o dano ao jogador e ativa o tremor
                if isinstance(ent2, Enemy):
                    ent2.apply_damage(ent1.damage)  # Aplica o dano ao jogador
                    ent2.tremer_duration = 20  # Ativa o tremor (20 frames)

                # Se o ent1 for um inimigo, aplica o dano ao inimigo
                if isinstance(ent1, Enemy):
                    ent1.apply_damage(ent2.damage)

                # Se o ent2 for um jogador, aplica o dano ao jogador e ativa o tremor
                if isinstance(ent2, Player):
                    ent2.apply_damage(ent1.damage)  # Aplica o dano ao jogador
                    ent2.tremer_duration = 20  # Ativa o tremor (20 frames)

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == "Player1Shot":
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score

        elif enemy.last_dmg == "Player2Shot":
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score


    @staticmethod
    def verify_health(entity_list: list[Entity], explosions: list):
        for ent in entity_list[:]:  # Itera sobre uma cópia da lista
            if ent.health <= 0 and ent.last_dmg != "Saída da tela":  # Verifica se a saúde do inimigo foi reduzida a 0 ou menos
                if isinstance(ent, Enemy):  # Se for um inimigo
                    EntityMediator.__give_score(ent, entity_list)
                    explosions.append(Explosion(ent.rect.centerx, ent.rect.centery))
                    pygame.mixer.Sound("./asset/explosion.wav").play()

                # Remove a entidade da lista
                entity_list.remove(ent)

        for ent in entity_list[:]:  # Itera sobre uma cópia da lista
            if ent.health <= 0:  # Verifica se a saúde do inimigo foi reduzida a 0 ou menos
                if isinstance(ent, Enemy):  # Se for um inimigo
                    EntityMediator.__give_score(ent, entity_list)

                # Remove a entidade da lista
                entity_list.remove(ent)
