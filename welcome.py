import pygame
from pygame.locals import *

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 1000
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

background = pygame.image.load('Images/Background scrolling camera.jpeg')
background = pygame.transform.scale(background, (display_width, display_height))

pygame.display.set_caption("Royal Hackaway Project")
icon = pygame.image.load('Images/gameIcon.gif')
pygame.display.set_icon(icon)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()

def text_objects(text, color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size= "small"):
    textSurf, textRect = text_objects(msg, color,size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)
    
def game_intro():
    intro = True
    while intro:
        gameDisplay.fill(white)
        message_to_screen("Welcome to our new game", green, -100, "large")
        message_to_screen("The objectives of the game is to teach you about sustainability.", black, -30)
        message_to_screen("Press (C) to continue and (Q) to quit", black, 40)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    gameExit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        pygame.display.update()

def gameLoop():
    gameExit = False

    while not gameExit:
        game_intro()

gameLoop()
pygame.quit()
exit()