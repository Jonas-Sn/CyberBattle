import pygame
from code.Const import ENTITY_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY
from code.EnemyShot import EnemyShot
from code.Entity import Entity
import random

class Enemy(Entity):

    def __init__(self, name:str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.tremer_duration = 0  # Duração do efeito de tremor
        self.tremer_offset = (0, 0)  # Deslocamento do tremor
        self.tremer_sound_played = False  # Para garantir que o som seja tocado apenas uma vez

    def move(self):
        # Verifica se o tremor está ativo
        if self.tremer_duration > 0:
            self.tremer_duration -= 1  # Diminui o tempo do tremor
            self.tremer_offset = (random.randint(-5, 5), random.randint(-5, 5))  # Altera a posição aleatoriamente
            # Toca o som apenas uma vez quando o tremor começa
            if not self.tremer_sound_played:
                pygame.mixer.Sound("./asset/hurt_sound.wav").play()  # Substitua pelo caminho correto
                self.tremer_sound_played = True
        else:
            self.tremer_offset = (0, 0)  # Desativa o tremor
            self.tremer_sound_played = False  # Reseta para poder tocar o som na próxima vez que o tremor ocorrer

        self.rect.x += self.tremer_offset[0]  # Aplica o efeito de tremor na posição
        self.rect.y += self.tremer_offset[1]  # Aplica o efeito de tremor na posição
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def apply_damage(self, damage: int):
        self.health -= damage
        self.tremer_duration = 10
        self.tremer_offset = (5, 0)
