import os
import random
from copy import copy
from random import randint

import pgzrun
from pgzero.clock import Clock
from pgzero.keyboard import Keyboard
from pgzero.rect import Rect
from pgzero.screen import Screen

WIDTH = 600
HEIGHT = 640

screen: Screen
keyboard: Keyboard
clock: Clock

BACKGROUND_COLOUR = (5, 20, 0)

HEADER_HEIGHT = 40
FOOTER_HEIGHT = 20
MARGIN_WIDTH = 20

SCORE_COLOUR = (0, 255, 0)
BORDER_COLOUR = (200, 0, 0)
BORDER_WIDTH = 3

LIVES_COLOUR = (200, 200, 0)
LIVES_RADIUS = 8
LIVES_SPACING = 5

STARTING_LIVES = 3

score = 0
level = 1
lives = STARTING_LIVES


def draw_score():
    screen.draw.text(f"{score}",
                     center=(WIDTH / 2, HEADER_HEIGHT / 2),
                     color=SCORE_COLOUR,
                     fontsize=36)


def draw_level():
    screen.draw.text(f"Level: {level}",
                     right=(WIDTH - MARGIN_WIDTH),
                     centery=HEADER_HEIGHT / 2,
                     color=SCORE_COLOUR,
                     fontsize=36)


def draw_border():
    left = MARGIN_WIDTH
    top = HEADER_HEIGHT
    width = WIDTH - (2 * MARGIN_WIDTH)
    height = HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT
    screen.draw.filled_rect(Rect(left, top, width, height), BORDER_COLOUR)

    left += BORDER_WIDTH
    top += BORDER_WIDTH
    width -= (2 * BORDER_WIDTH)
    screen.draw.filled_rect(Rect(left, top, width, height), BACKGROUND_COLOUR)


def draw_lives():
    for i in range(lives):
        x = MARGIN_WIDTH + LIVES_RADIUS + (i * (
            (2 * LIVES_RADIUS) + LIVES_SPACING))
        y = HEADER_HEIGHT / 2
        screen.draw.filled_circle((x, y), LIVES_RADIUS, LIVES_COLOUR)


def draw():
    screen.fill(BACKGROUND_COLOUR)

    draw_score()
    draw_level()
    draw_border()
    draw_lives()

    paddle.draw(screen.draw)


PADDLE_COLOUR = (200, 0, 0)
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 6
PADDLE_SPEED = 400


class Paddle:

    def __init__(self, pos):
        self.position = pos
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.colour = PADDLE_COLOUR

        # This is the speed the paddle can go left and right in pixels per second
        self.vx = PADDLE_SPEED

        # These are the bounds that the paddles box must stay within
        self.min_x = MARGIN_WIDTH + (PADDLE_WIDTH / 2)
        self.max_x = WIDTH - MARGIN_WIDTH - (PADDLE_WIDTH / 2)

    @property
    def bounding_box(self):
        half_width = int(self.width / 2)
        return Rect((self.x - half_width, self.y), (self.width, self.height))

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def draw(self, painter):
        painter.filled_rect(self.bounding_box, self.colour)

    def update(self, dt):
        if keyboard.left:
            self.x -= self.vx * dt
        if keyboard.right:
            self.x += self.vx * dt

        # Now keep it in bounds
        if self.x < self.min_x:
            self.x = self.min_x
        elif self.x > self.max_x:
            self.x = self.max_x


paddle = Paddle((WIDTH / 2, HEIGHT - FOOTER_HEIGHT))


def update(dt):
    paddle.update(dt)


pgzrun.go()
