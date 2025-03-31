import pygame.key
from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.PlayerShot import PlayerShot
import random


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.tremer_duration = 0  # Duração do tremor em frames
        self.tremer_offset = (0, 0)  # Deslocamento do tremor
        self.tremer_sound_played = False

    def move(self):
        # Verifica se o tremor está ativo
        if self.tremer_duration > 0:
            self.tremer_duration -= 1  # Diminui o tempo do tremor
            self.tremer_offset = (random.randint(-5, 5), random.randint(-5, 5))  # Altera a posição aleatoriamente
            if not self.tremer_sound_played:
                pygame.mixer.Sound("./asset/hurt_sound.wav").play()  # Substitua pelo caminho correto
                self.tremer_sound_played = True
        else:
            self.tremer_offset = (0, 0)  # Desativa o tremor quando o tempo expira
            self.tremer_sound_played = False

        # Movimento do jogador com efeito de tremor
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]

        # Aplica o efeito de tremor na posição
        self.rect.x += self.tremer_offset[0]
        self.rect.y += self.tremer_offset[1]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def apply_damage(self, damage: int):
        self.health -= damage
        if self.health > 0:
            self.tremer_duration = 10  # Tempo do tremor (10 frames)
