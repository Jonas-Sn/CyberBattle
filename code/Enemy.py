import pygame
from code.Const import ENTITY_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY
from code.EnemyShot import EnemyShot
from code.Entity import Entity

class Enemy(Entity):

    def __init__(self, name:str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.tremer_duration = 0  # Duração do efeito de tremor
        self.tremer_offset = (0, 0)  # Deslocamento do tremor

    def move(self):
        # Aplica o deslocamento do tremor se o tremor estiver ativo
        if self.tremer_duration > 0:
            self.rect.x += self.tremer_offset[0]
            self.rect.y += self.tremer_offset[1]
            self.tremer_duration -= 1  # Diminui a duração do tremor

        # Movimento padrão do inimigo
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def apply_damage(self, damage: int):
        # Aplica o dano ao inimigo
        self.health -= damage
        self.tremer_duration = 10  # Define a duração do tremor
        self.tremer_offset = (5, 0)  # Define o deslocamento do tremor (horizontal)
