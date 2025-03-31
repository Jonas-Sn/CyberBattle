from random import random

import pygame
import sys
import random

from pygame import Surface, Rect, K_ESCAPE, K_RETURN
from pygame.font import Font
from code.Const import C_WHITE, WIN_HEIGHT, WIN_WIDTH, TIMEOUT_STEP, EVENT_TIMEOUT, EVENT_ENEMY, C_GREEN, C_CIAN, \
    SPAWN_TIME, MENU_OPTION, TIMEOUT_LEVEL
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL  # 20 segundos
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.explosions = []  # Lista para armazenar explosões
        self.enemy_passed_count = 0  # Contador de inimigos que passaram da tela
        self.enemy_limit = 1  # Número limite de inimigos que podem passar antes de perder
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        player = EntityFactory.get_entity("Player1")
        player.score = player_score[0]
        self.entity_list.append(player)
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity("Player2")
            player.score = player_score[1]
            self.entity_list.append(player)
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        # Collisions
        EntityMediator.verify_collision(entity_list=self.entity_list)
        EntityMediator.verify_health(entity_list=self.entity_list,
                                     explosions=self.explosions)  # Passa a lista de explosões

        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)
                if ent.name == 'Player1':
                    self.level_text(14, f'Player1 - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
                if ent.name == 'Player2':
                    self.level_text(14, f'Player2 - Health: {ent.health} | Score: {ent.score}', C_CIAN, (10, 45))

                # Verificar se o inimigo passou da tela
                if isinstance(ent, Enemy) and ent.rect.top > WIN_HEIGHT:
                    self.enemy_passed_count += 1  # Aumenta o contador de inimigos que passaram
                    self.entity_list.remove(ent)  # Remove o inimigo da tela

            # Verifique a condição de derrota
            if self.enemy_passed_count >= self.enemy_limit:
                self.game_over_screen()  # Chama a tela de derrota
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score

                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True

                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        return

                # Verifica colisões e condições de derrota
                if EntityMediator.verify_collision(self.entity_list):
                    self.game_over_screen_ship()  # Exibe a tela de derrota
                    return False

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True

                if not found_player:
                    self.game_over_screen()  # Exibe a tela de derrota
                    return False

            for explosion in self.explosions[:]:
                explosion.move()
                explosion.draw(self.window)
                if explosion.health <= 0:
                    self.explosions.remove(explosion)

            # printed text
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps() :.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            #Collisions
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list, explosions=self.explosions)

    def game_over_screen(self):
        pygame.mixer_music.load('./asset/Level1.mp3')  # Carrega a música de Game Over
        pygame.mixer_music.play(-1)  # Toca a música em loop
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Game Over", True, C_WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 60))

        # Exibe a mensagem "Game Over"
        self.window.fill((0, 0, 0))  # Limpa a tela com fundo preto
        self.window.blit(text, text_rect)

        # Exibe a mensagem "Pressione qualquer tecla para voltar"
        font_small = pygame.font.SysFont("Arial", 30)
        message = font_small.render("Você Morreu!", True, C_WHITE)
        message_rect = message.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 30))
        self.window.blit(message, message_rect)

        font_small = pygame.font.SysFont("Arial", 30)
        message2 = font_small.render("ENTER para voltar", True, C_WHITE)
        message2_rect = message2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 70))
        self.window.blit(message2, message2_rect)

        pygame.display.flip()

        # Espera até que o jogador pressione uma tecla para voltar
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        return  # Sai da tela de Game Over e volta ao menu

    def game_over_screen_ship(self):
        pygame.mixer_music.load('./asset/Level1.mp3')  # Carrega a música de Game Over
        pygame.mixer_music.play(-1)  # Toca a música em loop
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Game Over", True, C_WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 60))

        # Exibe a mensagem "Game Over"
        self.window.fill((0, 0, 0))  # Limpa a tela com fundo preto
        self.window.blit(text, text_rect)

        # Exibe a mensagem "Pressione qualquer tecla para voltar"
        font_small = pygame.font.SysFont("Arial", 30)
        message = font_small.render("Deixou os inimigos passarem", True, C_WHITE)
        message_rect = message.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 30))
        self.window.blit(message, message_rect)

        font_small = pygame.font.SysFont("Arial", 30)
        message2 = font_small.render("ENTER para voltar", True, C_WHITE)
        message2_rect = message2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 70))
        self.window.blit(message2, message2_rect)


        pygame.display.flip()

        # Espera até que o jogador pressione uma tecla para voltar
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        return  # Sai da tela de Game Over e volta ao menu

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
