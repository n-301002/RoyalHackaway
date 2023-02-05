import pygame
from pygame.locals import *
from sprite import sprite

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

player = sprite.Player(1, 600)
# ball = game.Ball()


def player_movement():
    player.move()
    player.draw()


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

    player_movement()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
