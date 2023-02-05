import pygame
from pygame.locals import *
from Level3 import game

# initialise pygame
pygame.init()


# creating the screen
width, height = 1000, 600

screen = pygame.display.set_mode((width, height))

background = pygame.image.load('Images/Background scrolling camera.jpeg')
background = pygame.transform.scale(background, (width, height))

# title and icon
pygame.display.set_caption("Royal Hackaway Project")
icon = pygame.image.load('Images/gameIcon.gif')
pygame.display.set_icon(icon)

game = game.Game()


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

    game.player_movement(screen)
    game.adding_obstacles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
