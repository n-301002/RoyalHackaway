import pygame, random
from pygame.locals import *
import sprite
import spriteSheet as spriteSheet

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

PLAYER_CENTRE = (256, 256)
PLAYER_DIMS = (512, 512)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

cardboard_box = pygame.image.load('Images/cardboard_box.png').convert_alpha()
glass_bottle = pygame.image.load('Images/glass_bottle.png').convert_alpha()
glass_jar = pygame.image.load('Images/glass_jar.png').convert_alpha()
newspaper = pygame.image.load('Images/newspaper.png').convert_alpha()
plastic_bottle = pygame.image.load('Images/plastic_bottle.png').convert_alpha()
tin = pygame.image.load('Images/tin.png').convert_alpha()

recycle_item = pygame.image.load('Images/recycle_items.png').convert_alpha()
sprite_sheet = spriteSheet.SpriteSheet(recycle_item)


background = pygame.image.load('Images/Background scrolling camera.jpeg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# title and icon
pygame.display.set_caption("Royal Hackaway Project")
icon = pygame.image.load('Images/gameIcon.gif')
pygame.display.set_icon(icon)

player = sprite.Player(1, 600)


def player_movement():
    player.move()
    player.draw()


# game loop
running = True
bg_loop = 0

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (bg_loop, 0))
    screen.blit(background, (SCREEN_WIDTH + bg_loop, 0))
    if (bg_loop == -SCREEN_WIDTH):
        screen.blit(background, (SCREEN_WIDTH + bg_loop, 0))
        bg_loop = 0
    bg_loop -= 1

    player_movement()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
