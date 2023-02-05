import pygame
from pygame.locals import *

# initialise pygame
pygame.init()

# creating the screen
width, height = 1000, 750

screen = pygame.display.set_mode((width, height))

background = pygame.image.load('Images/Background scrolling camera.jpeg')
background = pygame.transform.scale(background, (width, height))

# title and icon
pygame.display.set_caption("Royal Hackaway Project")
icon = pygame.image.load('Images/gameIcon.gif')
pygame.display.set_icon(icon)

# instruction screen


def instructions():
    header = pygame.image.load('Images/Instructions/howToPlay.png')
    screen.blit(header, ((width/4)-50, 50))
    instructions = pygame.image.load('Images/Instructions/instructions.png')
    screen.blit(instructions, ((width/4)-25, (height/4) + 50))
    back = pygame.image.load('Images/Instructions/back.png')
    screen.blit(back, ((width/16), height - 100))
    nextbutton = pygame.image.load('Images/Instructions/next.png')
    screen.blit(nextbutton, ((13*(width/16)), height - 100))


# game loop
running = True
bg_loop = 0

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (bg_loop, 0))
    screen.blit(background, (width + bg_loop, 0))
    if (bg_loop == -width):
        screen.blit(background, (width + bg_loop, 0))
        bg_loop = 0
    bg_loop -= 1

    instructions()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
