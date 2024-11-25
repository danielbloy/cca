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

draw_funcs = []


def draw():
    screen.fill(BACKGROUND_COLOUR)
    for draw_func in draw_funcs:
        draw_func(screen.draw)


update_funcs = []


def update(dt):
    for update_func in update_funcs:
        update_func(dt)


HEADER_HEIGHT = 40
FOOTER_HEIGHT = 20
MARGIN_WIDTH = 20

SCORE_COLOUR = (0, 255, 0)

score = 0


def draw_score(draw):
    draw.text(f"{score}",
              center=(WIDTH / 2, HEADER_HEIGHT / 2),
              color=SCORE_COLOUR,
              fontsize=36)


draw_funcs.append(draw_score)

LEVEL_COLOUR = (0, 255, 0)

level = 1


def draw_level(draw):
    draw.text(f"Level: {level}",
              right=(WIDTH - MARGIN_WIDTH),
              centery=HEADER_HEIGHT / 2,
              color=LEVEL_COLOUR,
              fontsize=36)


draw_funcs.append(draw_level)

BORDER_COLOUR = (200, 0, 0)
BORDER_WIDTH = 3


def draw_border(draw):
    left = MARGIN_WIDTH
    top = HEADER_HEIGHT
    width = WIDTH - (2 * MARGIN_WIDTH)
    height = HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT
    draw.filled_rect(Rect(left, top, width, height), BORDER_COLOUR)

    left += BORDER_WIDTH
    top += BORDER_WIDTH
    width -= (2 * BORDER_WIDTH)
    draw.filled_rect(Rect(left, top, width, height), BACKGROUND_COLOUR)


draw_funcs.append(draw_border)

LIVES_COLOUR = (200, 200, 0)
LIVES_RADIUS = 8
LIVES_SPACING = 5

STARTING_LIVES = 3

lives = STARTING_LIVES


def draw_lives(draw):
    for i in range(lives):
        x = MARGIN_WIDTH + LIVES_RADIUS + (i * (
            (2 * LIVES_RADIUS) + LIVES_SPACING))
        y = HEADER_HEIGHT / 2
        draw.filled_circle((x, y), LIVES_RADIUS, LIVES_COLOUR)


draw_funcs.append(draw_lives)

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

    def draw(self, draw):
        draw.filled_rect(self.bounding_box, self.colour)

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

draw_funcs.append(paddle.draw)
update_funcs.append(paddle.update)

pgzrun.go()
