#C
import pygame

C_ORANGE = (255, 128, 0)
C_WHITE = (255, 255, 255)
C_YELLOW = (255, 255, 128)
C_GREEN = (0, 128, 0)
C_CIAN = (0, 128, 128)
C_PURPLE = (128, 0, 128)



#E
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2

ENTITY_SPEED =  {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 1,
    'Level1Bg3': 2,
    'Level1Bg4': 3,
    'Level1Bg5': 4,
    'Level1Bg6': 5,
    'Level1Bg7': 6,
    'Level1Bg8': 7,
    'Level1Bg9': 8,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 1,
    'Level2Bg3': 2,
    'Level2Bg4': 3,
    'Level2Bg5': 4,
    'Level2Bg6': 5,
    'Level2Bg7': 6,
    'Level2Bg8': 7,
    'Level3Bg0': 0,
    'Level3Bg1': 0,
    'Level3Bg2': 1,
    'Level3Bg3': 2,
    'Level3Bg4': 3,
    'Level3Bg5': 4,
    'Level3Bg6': 5,
    'Level3Bg7': 6,
    'Level4Bg0': 0,
    'Level4Bg1': 0,
    'Level4Bg2': 1,
    'Level4Bg3': 2,
    'Level4Bg4': 3,
    'Level4Bg5': 4,
    'Level4Bg6': 5,
    'Level4Bg7': 6,
    'Level4Bg8': 7,
    'Player1': 3,
    'Player1Shot': 5,
    'Player2': 3,
    'Player2Shot': 5,
    'Enemy1': 2,
    'Enemy1Shot': 5,
    'Enemy2': 2,
    'Enemy2Shot': 4,
}

ENTITY_HEALTH = {
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Level1Bg2': 999,
    'Level1Bg3': 999,
    'Level1Bg4': 999,
    'Level1Bg5': 999,
    'Level1Bg6': 999,
    'Level1Bg7': 999,
    'Level1Bg8': 999,
    'Level1Bg9': 999,
    'Level2Bg0': 999,
    'Level2Bg1': 999,
    'Level2Bg2': 999,
    'Level2Bg3': 999,
    'Level2Bg4': 999,
    'Level2Bg5': 999,
    'Level2Bg6': 999,
    'Level2Bg7': 999,
    'Level2Bg8': 999,
    'Level3Bg0': 999,
    'Level3Bg1': 999,
    'Level3Bg2': 999,
    'Level3Bg3': 999,
    'Level3Bg4': 999,
    'Level3Bg5': 999,
    'Level3Bg6': 999,
    'Level3Bg7': 999,
    'Level4Bg0': 999,
    'Level4Bg1': 999,
    'Level4Bg2': 999,
    'Level4Bg3': 999,
    'Level4Bg4': 999,
    'Level4Bg5': 999,
    'Level4Bg6': 999,
    'Level4Bg7': 999,
    'Level4Bg8': 999,
    'Player1': 250,
    'Player1Shot': 1,
    'Player2': 250,
    'Player2Shot': 1,
    'Enemy1': 110,
    'Enemy1Shot': 1,
    'Enemy2': 130,
    'Enemy2Shot': 1,
    'Explosion': 999,
}

ENTITY_SHOT_DELAY = {
    'Player1': 20,
    'Player2': 20,
    'Enemy1': 100,
    'Enemy2': 100,
}

ENTITY_DAMAGE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level1Bg7': 0,
    'Level1Bg8': 0,
    'Level1Bg9': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Level2Bg5': 0,
    'Level2Bg6': 0,
    'Level2Bg7': 0,
    'Level2Bg8': 0,
    'Level3Bg0': 0,
    'Level3Bg1': 0,
    'Level3Bg2': 0,
    'Level3Bg3': 0,
    'Level3Bg4': 0,
    'Level3Bg5': 0,
    'Level3Bg6': 0,
    'Level3Bg7': 0,
    'Level4Bg0': 0,
    'Level4Bg1': 0,
    'Level4Bg2': 0,
    'Level4Bg3': 0,
    'Level4Bg4': 0,
    'Level4Bg5': 0,
    'Level4Bg6': 0,
    'Level4Bg7': 0,
    'Level4Bg8': 0,
    'Player1': 1,
    'Player1Shot': 20,
    'Player2': 1,
    'Player2Shot': 20,
    'Enemy1': 1,
    'Enemy1Shot': 15,
    'Enemy2': 1,
    'Enemy2Shot': 20,
    'Explosion': 0,
}

ENTITY_SCORE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level1Bg7': 0,
    'Level1Bg8': 0,
    'Level1Bg9': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Level2Bg5': 0,
    'Level2Bg6': 0,
    'Level2Bg7': 0,
    'Level2Bg8': 0,
    'Level3Bg0': 0,
    'Level3Bg1': 0,
    'Level3Bg2': 0,
    'Level3Bg3': 0,
    'Level3Bg4': 0,
    'Level3Bg5': 0,
    'Level3Bg6': 0,
    'Level3Bg7': 0,
    'Level4Bg0': 0,
    'Level4Bg1': 0,
    'Level4Bg2': 0,
    'Level4Bg3': 0,
    'Level4Bg4': 0,
    'Level4Bg5': 0,
    'Level4Bg6': 0,
    'Level4Bg7': 0,
    'Level4Bg8': 0,
    'Player1': 0,
    'Player1Shot': 0,
    'Player2': 0,
    'Player2Shot': 0,
    'Enemy1': 100,
    'Enemy1Shot': 0,
    'Enemy2': 125,
    'Enemy2Shot': 0,
    'Explosion': 0,  # Saúde para a explosão
}


#M
MENU_OPTION = ("NOVO JOGO 1P",
               "NOVO JOGO 2P - COOPERATIVO",
               "NOVO JOGO 2P - COMPETITIVO",
               "PONTUAÇÃO",
               "SAIR")
#P
PLAYER_KEY_UP = {'Player1': pygame.K_UP,
                 'Player2': pygame.K_w}

PLAYER_KEY_DOWN = {'Player1': pygame.K_DOWN,
                'Player2': pygame.K_s}

PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT,
                 'Player2': pygame.K_d}

PLAYER_KEY_LEFT = {'Player1': pygame.K_LEFT,
                 'Player2': pygame.K_a}

PLAYER_KEY_SHOOT = {'Player1': pygame.K_RCTRL,
                    'Player2': pygame.K_LCTRL}


# T

TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 60000

# W

WIN_WIDTH = 576
WIN_HEIGHT = 324

# S
SPAWN_TIME = 1500

SCORE_POS = {'Title': (WIN_WIDTH / 2, 50),
             'EnterName': (WIN_WIDTH / 2, 80),
             'Label': (WIN_WIDTH / 2, 90),
             'Name': (WIN_WIDTH / 2, 110),
             0: (WIN_WIDTH / 2, 110),
             1: (WIN_WIDTH / 2, 130),
             2: (WIN_WIDTH / 2, 150),
             3: (WIN_WIDTH / 2, 170),
             4: (WIN_WIDTH / 2, 190),
             5: (WIN_WIDTH / 2, 210),
             6: (WIN_WIDTH / 2, 230),
             7: (WIN_WIDTH / 2, 250),
             8: (WIN_WIDTH / 2, 270),
             9: (WIN_WIDTH / 2, 290),
             }
