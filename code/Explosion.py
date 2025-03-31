import pygame
from code.Entity import Entity
from code.Const import ENTITY_SPEED

class Explosion(Entity):
    def __init__(self, x, y):
        super().__init__('Explosion', (x, y))
        self.surf = pygame.transform.scale(self.surf, (1, 1))
        self.rect = self.surf.get_rect(center=(x, y))
        self.explosion_sound = pygame.mixer.Sound('./asset/explosion.wav')
        self.explosion_sound.play()  # Reproduz o som da explosão
        self.frames = [
            pygame.image.load(f'./asset/explosion{i}.png').convert_alpha()
            for i in range(1, 6)
        ]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0
        self.frame_delay = 5  # velocidade da animação

    def move(self):
        self.timer += 1
        if self.timer % self.frame_delay == 0:
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.health = 0  # Remove a explosão

    def draw(self, window):
        window.blit(self.image, self.rect)
