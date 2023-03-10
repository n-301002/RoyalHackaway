import pygame
import random
import vector as Vector
import sprite as Sprite
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

WIDTH = 1000
HEIGHT = 750

PLAYER_CENTRE = (256, 256)
PLAYER_DIMS = (512, 512)

# Score and lives counter for each player
SCORE_PLAYER1 = 0
LIVES_PLAYER1 = 5


# Booleans for game mechanism
GAME_BEGIN = False
GAME_OVER = False
GAME_HELP = False
GAME_START = False

# Defining random global methods


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


class Boundary:
    def __init__(self, limit, border, colour):
        self.limit = limit
        self.border = border * 2
        self.colour = colour
        self.normal = Vector(1, 0)
        self.edge_r = limit + self.border

    def draw_boundary(self, screen):
        x1 = (0, 4*HEIGHT/5)
        x2 = (WIDTH, 4*HEIGHT/5)
        pygame.draw.line(screen, 'grey', x1, x2, 1)


# Logic of the game: Interaction between player and collisions/obstacles
class Interaction:
    def __init__(self, player, wall):
        self.player = player
        self.wall = wall
        self.good_balls = []
        self.bad_balls = []
        self.multiplier = []
        self.extra_life = []
        self.in_collision = False
        self.to_remove = []
        self.already_collided = set()

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

    def adding_balls(self):
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

    def collide(self, ball, player):
        normal = ball.position.copy().subtract(player.position).normalize()

        vel1_par = ball.velocity.get_proj(normal)
        vel1_perp = ball.velocity.copy().subtract(vel1_par)
        vel2_par = player.velocity.get_proj(normal)
        vel2_perp = player.velocity.copy().subtract(vel2_par)

        ball.velocity = vel2_par + vel1_perp
        player.velocity = vel1_par + vel2_perp

    def player_collision(self):
        global SCORE_PLAYER1, LIVES_PLAYER1, GAME_OVER
        for good_ball in self.good_balls:
            if good_ball.has_collided(self.player):
                sticky1 = (good_ball, self.player) in self.already_collided
                sticky2 = (self.player, good_ball) in self.already_collided
                if not (sticky1 or sticky2):
                    if not self.in_collision:
                        self.collide(good_ball, self.player)
                        self.already_collided.add((good_ball, self.player))
                        self.in_collision = True
                        if LIVES_PLAYER1 > 0:
                            if SCORE_PLAYER1 < 30:
                                SCORE_PLAYER1 += 1
                                # BLUE_SOUND.play()
                                self.to_remove.append(good_ball)
                        else:
                            GAME_OVER = True
                    else:
                        self.in_collision = False
                else:
                    self.already_collided.discard(sticky1)
                    self.already_collided.discard(sticky2)

        for bad_ball in self.bad_balls:
            if bad_ball.has_collided(self.player):
                sticky1 = (bad_ball, self.player) in self.already_collided
                sticky2 = (self.player, bad_ball) in self.already_collided
                if not (sticky1 or sticky2):
                    if not self.in_collision:
                        self.collide(bad_ball, self.player)
                        self.already_collided.add((bad_ball, self.player))
                        self.in_collision = True
                        if LIVES_PLAYER1 > 0:
                            if SCORE_PLAYER1 < 30:
                                LIVES_PLAYER1 -= 1
                                # RED_SOUND.play()
                                self.to_remove.append(bad_ball)
                        else:
                            GAME_OVER = True
                    else:
                        self.in_collision = False
                else:
                    self.already_collided.discard(sticky1)
                    self.already_collided.discard(sticky2)

        for multiplier in self.multiplier:
            if multiplier.has_collided(self.player):
                sticky1 = (multiplier, self.player) in self.already_collided
                sticky2 = (self.player, multiplier) in self.already_collided
                if not (sticky1 or sticky2):
                    if not self.in_collision:
                        self.collide(multiplier, self.player)
                        self.already_collided.add((multiplier, self.player))
                        self.in_collision = True
                        if LIVES_PLAYER1 > 0:
                            if SCORE_PLAYER1 < 30:
                                SCORE_PLAYER1 += 3
                                # GREEN_SOUND.play()
                                self.to_remove.append(multiplier)
                        else:
                            GAME_OVER = True
                    else:
                        self.in_collision = False
                else:
                    self.already_collided.discard(sticky1)
                    self.already_collided.discard(sticky2)

        for extra_life in self.extra_life:
            if extra_life.has_collided(self.player):
                sticky1 = (extra_life, self.player) in self.already_collided
                sticky2 = (self.player, extra_life) in self.already_collided
                if not (sticky1 or sticky2):
                    if not self.in_collision:
                        self.collide(extra_life, self.player)
                        self.already_collided.add((extra_life, self.player))
                        self.in_collision = True
                        if LIVES_PLAYER1 > 0:
                            if SCORE_PLAYER1 < 30:
                                if LIVES_PLAYER1 < 5:
                                    LIVES_PLAYER1 += 1
                                    # LIFE_SOUND.play()
                                    self.to_remove.append(extra_life)
                        else:
                            GAME_OVER = True
                    else:
                        self.in_collision = False
                else:
                    self.already_collided.discard(sticky1)
                    self.already_collided.discard(sticky2)

    def wrap_player(self, canvas):
        if self.player.position.get_p()[0] > WIDTH - self.player.radius:
            self.player.position = Vector(-self.player.radius,
                                          self.player.position.get_p()[1])
        elif self.player.position.get_p()[0] < -self.player.radius:
            self.player.position = Vector(
                WIDTH - self.player.radius, self.player.position.get_p()[1])
        elif self.player.position.get_p()[1] > HEIGHT + self.player.radius:
            self.player.position = Vector(self.player.position.get_p()[
                                          0], -self.player.radius)
        elif self.player.position.get_p()[1] < -self.player.radius:
            self.player.position = Vector(self.player.position.get_p()[
                                          0], HEIGHT + self.player.radius)
        else:
            self.player.draw(canvas)

    def update(self, canvas):
        self.wrap_player(canvas)
        self.player.update()
        self.player.move()


class Game:
    def __init__(self):
        self.player = Sprite.Player(WIDTH//2, HEIGHT//2)
        self.wall = Boundary(0, 1, 'Grey')
        self.interaction = Interaction(self.player1, self.wall)
        self.game_on = False

    def draw(self, canvas):
        self.interaction.player_collision()
        self.interaction.update(canvas)

    def update(self, canvas):
        global GAME_BEGIN, LIVES_PLAYER1, SCORE_PLAYER1
        if LIVES_PLAYER1 < 1:
            self.game_on = False
            if LIVES_PLAYER2 < 1:
                self.player1_won(canvas)

        elif SCORE_PLAYER1 > 29:
            self.game_on = False
            if SCORE_PLAYER1 > 29:
                self.player1_won(canvas)

        else:
            self.game_on = True
            self.draw(canvas)
            if self.click() == False:
                self.reset()

        return GAME_BEGIN

    def set_score(self):
        global LIVES_PLAYER1, LIVES_PLAYER2, SCORE_PLAYER1, SCORE_PLAYER2
        LIVES_PLAYER1 = 5
        LIVES_PLAYER2 = 5
        SCORE_PLAYER1 = 0
        SCORE_PLAYER2 = 0

    def reset(self):
        global GAME_BEGIN, GAME_HELP, LIVES_PLAYER1, LIVES_PLAYER2, SCORE_PLAYER1, SCORE_PLAYER2
        if GAME_BEGIN == True:
            self.set_score()
            GAME_BEGIN = False

        return GAME_BEGIN

    def adding_obstacles(self):
        if self.game_on == True:
            self.interaction.adding_balls()
        else:
            self.clear_canvas()

    def clear_canvas(self):
        if self.interaction.is_ball_on_canvas() == True:
            self.interaction.removing_balls()

    def game_mode(self, canvas):
        self.background.draw(canvas)
        self.welcome.player_mode(canvas)
        self.click()

    def start(self, canvas):
        self.background.draw(canvas)
        self.welcome.draw(canvas)
        self.set_score()

    def help_screen(self, canvas):
        self.background.draw(canvas)
        self.welcome.instruction_screen(canvas)

    def player1_won(self, canvas):
        global GAME_BEGIN, count
        # WIN_SOUND.play()
        count += 1
        self.background.draw(canvas)
        self.welcome.player1_won(canvas)
        if self.click() == False or count % 300 == 0:
            self.instruction_help()
            self.reset()
        return GAME_BEGIN
