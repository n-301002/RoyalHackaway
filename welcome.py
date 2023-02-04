# This is the main file where the game will be run from
import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Welcome to the new Game!!')
img = pygame.image.load('Images/tree.png')

font = pygame.font.SysFont(None, 25)


def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2, display_height/2])


def gameLoop():
    gameExit = False
    gameOver = False

    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen(
                "Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, [400, 300, 50, 50])

        pygame.display.update()


gameLoop()

pygame.quit()
quit()

clock = pygame.time.Clock()


def game_intro():
    intro = True
    while intro:
        gameDisplay.fill(white)
        message_to_screen
