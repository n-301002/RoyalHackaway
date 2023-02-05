import pygame
from pygame.locals import *
import random
from Level3 import vector as Vector
from sprite.sprite import sprite

pygame.init()

WIDTH = 1000
HEIGHT = 750


def rand_pos():
    x = [HEIGHT/4, (3*HEIGHT)/4]
    return random.choice(x)


def rand_rad():
    return random.randint(10, 21)


def rand_vel():
    return random.randint(-5, 5)


def rand_vel_pos():
    return random.randint(0, 6)


class Ball:
    def __init__(self, position, velocity, colour):
        self.position = position
        self.velocity = velocity
        self.radius = rand_rad()
        self.border = 1
        self.colour = colour

    def update(self):
        self.position.add(self.velocity)

    def has_collided(self, player):
        collision = player.position.copy().subtract(self.position).length()
        return collision < player.radius + self.radius

    def draw(self, screen):
        self.update()
        pygame.draw.circle(screen, self.colour,
                           self.position.get_p(), self.radius)


class Interaction:

    def add_good_ball(self):
        p = Vector(WIDTH+20, rand_pos())
        v = Vector(rand_vel(), rand_vel_pos())
        good_ball = Ball(p, v, rand_rad(), '#3D5DE0')
        self.good_balls.append(good_ball)

    def add_bad_ball(self):
        p = Vector(WIDTH+20, rand_pos())
        v = Vector(0.9*rand_vel(), 0.9*rand_vel_pos())
        bad_ball = Ball(p, v, rand_rad(), '#D50D3A')
        self.bad_balls.append(bad_ball)

    def add_multiplier(self):
        p = Vector(WIDTH+20, rand_pos())
        v = Vector(1.5*rand_vel(), 1.5*rand_vel_pos())
        multiplier = Ball(p, v, rand_rad(), '#01754A')
        self.multiplier.append(multiplier)

    def add_extra_life(self):
        p = Vector(WIDTH+20, rand_pos())
        v = Vector(2*rand_vel(), 2*rand_vel_pos())
        extra_life = Ball(p, v, rand_rad(), '#F776C6')
        self.extra_life.append(extra_life)

    def removing_balls(self):
        for ball in self.to_remove:
            if ball in self.good_balls:
                self.good_balls.remove(ball)
            elif ball in self.bad_balls:
                self.bad_balls.remove(ball)
            elif ball in self.multiplier:
                self.multiplier.remove(ball)
            elif ball in self.extra_life:
                self.extra_life.remove(ball)

    def emerge(self):
        self.add_good_ball()
        if len(self.good_balls) % 3 == 0:
            self.add_bad_ball()
            self.removing_balls()
        if len(self.good_balls) % 10 == 0:
            self.add_multiplier()
            self.removing_balls()
        if len(self.good_balls) % 20 == 0:
            self.add_extra_life()
            self.removing_balls()
