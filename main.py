from tkinter import *
import pygame


# initialise pygame
pygame.init()

# creating the screen
width = 1000
height = 750

screen = pygame.display.set_mode((width, height))

background = pygame.image.load('RH sprites/Background scrolling camera.jpg')
backgorund = pygame.transform.scale(background, (width, height))

# title and icon
pygame.display.set_caption("Royal Hackaway Project")
icon = pygame.image.load('RH sprites/gameIcon.gif')
pygame.display.set_icon(icon)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


class Instruction:
    pass
