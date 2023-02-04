from tkinter import *
import pygame


# initialise pygame
pygame.init()
# creating the screen
screen = pygame.display.set_mode((1000, 750))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


class Instruction:
    pass
