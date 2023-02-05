import pygame, sys

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = pygame.image.load('Images/lvl1-background.png').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (BACKGROUND.get_width()/3, BACKGROUND.get_height()/3))

class GameState:
    def __init__(self):
        self.state = 'main_game'
    
    def lvl_one(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.blit(BACKGROUND, (0,0))
    



game_state = GameState()

run = True
while True:
    game_state.lvl_one()
    
    
    
    pygame.display.update()
    