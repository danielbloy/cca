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


pgzrun.go()
