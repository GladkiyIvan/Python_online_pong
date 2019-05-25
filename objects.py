import pygame
from random import choice


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 1.5

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, direction):
        if direction == 'up' and self.y > 0:
            self.y -= self.vel
        elif direction == 'down' and self.y < (720 - self.height):
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


class Ball():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = (x, y, size, size)
        self.y_vel = choice([1, -1])
        self.x_vel = choice([1, -1])

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def change_direction(self, axis):
        if axis == 0:
            self.x_vel *= -1
        elif axis == 1:
            self.y_vel *= -1

    def update(self):
        self.x += self.x_vel
        if self.x == 0 or self.x == 1000 - self.size:
            self.change_direction(0)

        self.y += self.y_vel
        if self.y == 0 or self.y == 720 - self.size:
            self.change_direction(1)

        self.rect = (self.x, self.y, self.size, self.size)


class Game():
    def __init__(self, players, ball, winner, p1_scored, p2_scored, is_goal=False):
        self.players = players
        self.ball = ball
        self.winner = winner
        self.p1_scored = p1_scored
        self.p2_scored = p2_scored
        self.p1_ready = False
        self.p2_ready = False
        self.is_finished = False
        self.is_goal = is_goal
        self.play_sound = False

    def update(self, direction, player):
        self.players[player].move(direction)
        self.ball.update()
        self.try_pong()
        self.try_goal()
        if self.is_goal:
            self.players = [Player(45, 285, 10, 150, (255, 255, 255)), Player(945, 285, 10, 150, (255, 255, 255))]
            self.ball = Ball(465, 330, 25, (255, 255, 255))

    def draw(self, win):
        self.players[0].draw(win)
        self.players[1].draw(win)
        self.ball.draw(win)

    def try_pong(self):

        if (((self.players[0].y + self.players[0].height) >= self.ball.y >= self.players[0].y) or
            ((self.players[0].y + self.players[0].height) >= self.ball.y + self.ball.size >= self.players[0].y)) \
                and self.ball.x == self.players[0].x + self.players[0].width:
            self.ball.change_direction(0)
            self.play_sound = True
            return

        if (((self.players[1].y + self.players[1].height) >= self.ball.y >= self.players[1].y) or
            ((self.players[1].y + self.players[1].height) >= self.ball.y + self.ball.size >= self.players[1].y)) \
                and self.ball.x == self.players[1].x - self.ball.size:
            self.ball.change_direction(0)
            self.play_sound = True
            return

    def try_goal(self):

        if self.ball.x == 0:
            self.p2_scored += 1
            self.play_sound = True
            self.is_goal = True

        elif self.ball.x == 1000 - self.ball.size:
            self.p1_scored += 1
            self.play_sound = True
            self.is_goal = True

        if self.p1_scored == 7 or self.p2_scored == 7:
            self.winner = 0 if self.p1_scored == 7 else 1
            self.play_sound = False
            self.is_finished = True
