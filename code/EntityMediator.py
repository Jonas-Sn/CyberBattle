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
    enemy_limit = 2  # Número limite de inimigos que podem passar antes de perder

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:  # O inimigo saiu da tela
                if ent.health > 0:  # Evita contar inimigos já destruídos
                    ent.health = 0  # Define a saúde para 0
                    ent.last_dmg = "Saída da tela"  # Marca que a destruição foi por saída da tela
                    EntityMediator.enemy_passed_count += 1  # Aumenta o contador de inimigos que passaram
                    print(f"Inimigos passados: {EntityMediator.enemy_passed_count}/{EntityMediator.enemy_limit}")  # Debug

                # Remove o inimigo imediatamente para evitar contagem repetida
                return True if EntityMediator.enemy_passed_count >= EntityMediator.enemy_limit else False

        if isinstance(ent, PlayerShot) and ent.rect.left >= WIN_WIDTH:
            ent.health = 0

        if isinstance(ent, EnemyShot) and ent.rect.right <= 0:
            ent.health = 0

        return False

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        game_over = False
        for entity in entity_list[:]:  # Itera sobre uma cópia da lista
            if EntityMediator.__verify_collision_window(entity):
                game_over = True  # Marca que o game over deve ocorrer
            for other_entity in entity_list[:]:  # Evita erros de índice ao modificar a lista
                if entity != other_entity:
                    EntityMediator.__verify_collision_entity(entity, other_entity)

        return game_over  # Retorna True apenas se a condição de derrota for atingida

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

                # Se o ent1 for um jogador, aplica o dano
                if isinstance(ent1, Player):
                    ent1.apply_damage(ent2.damage)

                # Se o ent2 for um inimigo, aplica o dano e ativa o tremor
                if isinstance(ent2, Enemy):
                    ent2.apply_damage(ent1.damage)
                    ent2.tremer_duration = 20

                # Se o ent1 for um inimigo, aplica o dano
                if isinstance(ent1, Enemy):
                    ent1.apply_damage(ent2.damage)

                # Se o ent2 for um jogador, aplica o dano e ativa o tremor
                if isinstance(ent2, Player):
                    ent2.apply_damage(ent1.damage)
                    ent2.tremer_duration = 20

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
            if ent.health <= 0 and ent.last_dmg != "Saída da tela":
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                    explosions.append(Explosion(ent.rect.centerx, ent.rect.centery))
                    pygame.mixer.Sound("./asset/explosion.wav").play()

                entity_list.remove(ent)  # Remove a entidade imediatamente
