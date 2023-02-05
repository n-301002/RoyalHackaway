import pygame
from pygame.locals import *
import random
from Level3 import vector
from Sprites import sprite

pygame.init()


WIDTH = 1000
HEIGHT = 600


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
    def __init__(self, position, velocity, radius, colour):
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
    def __init__(self) -> None:
        self.player = sprite.Player(1, 480)
        self.good_balls = []
        self.bad_balls = []
        self.multiplier = []
        self.extra_life = []
        self.in_collision = False
        self.to_remove = []
        self.already_collided = set()

    def add_good_ball(self):
        p = vector.Vector(WIDTH+20, rand_pos())
        v = vector.Vector(rand_vel(), rand_vel_pos())
        good_ball = Ball(p, v, rand_rad(), '#3D5DE0')
        self.good_balls.append(good_ball)

    def add_bad_ball(self):
        p = vector.Vector(WIDTH+20, rand_pos())
        v = vector.Vector(0.9*rand_vel(), 0.9*rand_vel_pos())
        bad_ball = Ball(p, v, rand_rad(), '#D50D3A')
        self.bad_balls.append(bad_ball)

    def add_multiplier(self):
        p = vector.Vector(WIDTH+20, rand_pos())
        v = vector.Vector(1.5*rand_vel(), 1.5*rand_vel_pos())
        multiplier = Ball(p, v, rand_rad(), '#01754A')
        self.multiplier.append(multiplier)

    def add_extra_life(self):
        p = vector.Vector(WIDTH+20, rand_pos())
        v = vector.Vector(2*rand_vel(), 2*rand_vel_pos())
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

    def update_ball(self, screen):
        for good_ball in self.good_balls:
            good_ball.draw(screen)
            good_ball.update()
        for bad_ball in self.bad_balls:
            bad_ball.draw(screen)
            bad_ball.update()
        for multiplier in self.multiplier:
            multiplier.draw(screen)
            multiplier.update()
        for extra_life in self.extra_life:
            extra_life.draw(screen)
            extra_life.update()

    def draw_ball(self, screen):
        self.update_ball(screen)
        self.removing_balls()

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

    def player_movement(self):
        self.player.move()
        self.player.draw()

    def is_ball_on_canvas(self):
        for good_ball in self.good_balls:
            if good_ball.position.y - good_ball.radius < HEIGHT:
                return False
            else:
                self.to_remove.append(good_ball)
        for bad_ball in self.bad_balls:
            if bad_ball.position.y - bad_ball.radius < HEIGHT:
                return False
            else:
                self.to_remove.append(bad_ball)
        for multiplier in self.multiplier:
            if multiplier.position.y - multiplier.radius < HEIGHT:
                return False
            else:
                self.to_remove.append(multiplier)
        for extra_life in self.extra_life:
            if extra_life.position.y - extra_life.radius < HEIGHT:
                return False
            else:
                self.to_remove.append(extra_life)

        return True

    def wrap_player(self, canvas):
        if self.player.position.get_p()[0] > WIDTH - self.player.radius:
            self.player.position = vector.Vector(-self.player.radius,
                                                 self.player.position.get_p()[1])
        elif self.player.position.get_p()[0] < -self.player.radius:
            self.player.position = vector.Vector(
                WIDTH - self.player.radius, self.player.position.get_p()[1])
        elif self.player.position.get_p()[1] > HEIGHT + self.player.radius:
            self.player.position = vector.Vector(self.player.position.get_p()[
                0], -self.player.radius)
        elif self.player.position.get_p()[1] < -self.player.radius:
            self.player.position = vector.Vector(self.player.position.get_p()[
                0], HEIGHT + self.player.radius)
        else:
            self.player.draw(canvas)


class Game:
    def __init__(self) -> None:
        self.interaction = Interaction()
        self.game_on == True

    def player_movement(self, screen):
        self.interaction.player_movement()
        self.interaction.draw_ball(screen)

    def adding_obstacles(self):
        if self.game_on == True:
            self.interaction.emerge()
        else:
            self.clear_canvas()

    def clear_canvas(self):
        if self.interaction.is_ball_on_canvas() == True:
            self.interaction.removing_balls()

    def update(self, canvas):
        global GAME_BEGIN, LIVES_PLAYER, SCORE_PLAYER
        if LIVES_PLAYER1 < 1:
            GAME_OVER = True
            GAME_START = False
            self.game_on = False
            if LIVES_PLAYER2 < 1:
                self.player1_won(canvas)
            elif LIVES_PLAYER1 < 1:
                self.player2_won(canvas)

        elif SCORE_PLAYER1 > 29 or SCORE_PLAYER2 > 29:
            GAME_OVER = True
            GAME_START = False
            self.game_on = False
            if SCORE_PLAYER1 > 29:
                self.player1_won(canvas)
            elif SCORE_PLAYER2 > 29:
                self.player2_won(canvas)

        else:
            self.game_on = True
            GAME_OVER = False
            self.draw(canvas)
            if self.click() == False:
                GAME_BEGIN = True
                GAME_START = False
                self.reset()

        return GAME_BEGIN
