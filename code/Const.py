# font file
import pygame

FONT_MAIN = './assets/fonts/acknowtt.ttf'

# colors
C_BLACK = (0, 0, 0)
C_GRAY = (127, 127, 127)
C_WHITE = (255, 255, 255)

# shadow
SHADOW_COLOR = C_GRAY
SHADOW_DIRECTION = (1, 1)

# sizes
WINDOW_SIZE = (800, 480)
LOGO_SIZE = (200, 200)
TITLE_SIZE = 200
SIGN_SIZE = 20
MAP_TOPLEFT = (30, 30)
MAP_BOTTOMRIGHT = (WINDOW_SIZE[0] - 130, WINDOW_SIZE[1] - 50)

# main menu
MENU_HEIGHT = WINDOW_SIZE[1] / 1.8
MENU_SPACING = 40
MENU_OPTION_SIZE = 70
MENU_OPTION = (
    'ONE PLAYER',
    'TWO PLAYERS',
    'CONSTRUCTION',
    'QUIT'
)

# global level settings
LEVEL_FPS = 60

# entity defaults
PLAYER_HEALTH = 300
PLAYER_SHOT_DELAY = 30
PLAYER_SPEED = 2

ENEMY_HEALTH = {
    'enemy1' : 100,
    'enemy2' : 200,
    'enemy3' : 500,
}

ENEMY_SPEED = {
    'enemy1' : 2,
    'enemy2' : 1,
    'enemy3' : 0.25,
}

ENEMY_SHOT_DELAY = {
    'enemy1' : 30,
    'enemy2' : 20,
    'enemy3' : 15,
}

ENEMY_RANDOM_MOVEMENT_DELAY = {
    'enemy1' : 5,
    'enemy2' : 10,
    'enemy3' : 15,
}

SHOT_SPEED = 4
SHOT_DAMAGE = 50

# key binding
KEY_UP = \
    {
        'player1': pygame.K_w,
        'player2': pygame.K_UP
    }

KEY_DOWN = \
    {
        'player1': pygame.K_s,
        'player2': pygame.K_DOWN
    }

KEY_LEFT = \
    {
        'player1': pygame.K_a,
        'player2': pygame.K_LEFT
    }
KEY_RIGHT = \
    {
        'player1': pygame.K_d,
        'player2': pygame.K_RIGHT
    }
KEY_SHOOT = \
    {
        'player1': pygame.K_SPACE,
        'player2': pygame.K_KP_PLUS
    }