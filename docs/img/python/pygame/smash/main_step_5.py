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
    ball.draw(screen.draw)

    if serving:
        screen.draw.text(f"Level {level}",
                         center=(WIDTH / 2, HEIGHT / 2),
                         color=SCORE_COLOUR,
                         fontsize=72)
        screen.draw.text("Press space to serve",
                         center=(WIDTH / 2, HEIGHT * 3 / 4),
                         color=SCORE_COLOUR,
                         fontsize=36)
    for block in blocks:
        block.draw(screen.draw)


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

BALL_RADIUS = 6
BALL_COLOUR = (200, 200, 0)
BALL_SPEED_Y = 500
BALL_SPIN_X_MIN = 100
BALL_SPIN_X_MAX = 200


class Ball:

    def __init__(self, pos):
        self.position = pos
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        self.colour = BALL_COLOUR
        self.min_x = MARGIN_WIDTH + BORDER_WIDTH + BALL_RADIUS
        self.max_x = WIDTH - MARGIN_WIDTH - BORDER_WIDTH - BALL_RADIUS
        self.min_y = HEADER_HEIGHT + BORDER_WIDTH + BALL_RADIUS
        self.max_y = HEIGHT

    @property
    def bounding_box(self):
        x = self.x - self.radius
        y = self.y - self.radius
        width = 2 * self.radius
        height = 2 * self.radius
        return Rect(x, y, width, height)

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def draw(self, painter):
        painter.filled_circle(self.position, self.radius, self.colour)

    def update(self, dt):
        # Move the ball and keep it in bounds.
        self.x += (self.vx * dt)
        self.y += (self.vy * dt)

        if self.x < self.min_x:
            self.x = self.min_x
            self.vx *= -1
        elif self.x > self.max_x:
            self.x = self.max_x
            self.vx *= -1

        if self.y < self.min_y:
            self.y = self.min_y
            self.vy *= -1
        elif self.y > self.max_y:
            self.y = self.max_y
            self.vy *= -1

    def stop(self):
        self.vx = 0
        self.vy = 0

    def serve(self):
        self.hit(-BALL_SPEED_Y)

    def bounce(self):
        self.hit(self.vy * -1)

    def hit(self, vertical_speed):
        self.vy = vertical_speed
        spin = random.randint(BALL_SPIN_X_MIN, BALL_SPIN_X_MAX)
        if keyboard.left:
            self.vx -= spin
        else:
            self.vx += spin

    def collide(self, rect) -> bool:
        return self.bounding_box.colliderect(rect)


ball = Ball(paddle.position)


def update(dt):
    paddle.update(dt)
    ball.update(dt)

    if not playing and keyboard.space:
        start_game()

    if serving:
        serve_ball()


playing = False
serving = True
game_over = False


def start_game():
    global score, level, lives, playing, serving, game_over
    score = 0
    level = 1
    lives = STARTING_LIVES
    playing = True
    serving = True
    game_over = False
    setup_blocks()


def serve_ball():
    global serving, ball

    # If we are serving, keep the ball with the paddle.
    ball.position = paddle.position

    # If space is pressed, serve the ball
    if keyboard.space:
        serving = False
        ball.serve()


class Block:

    def __init__(self, rect, colour, value):
        self.rect = rect
        self.colour = colour
        self.value = value

    @property
    def bounding_box(self):
        return self.rect

    @property
    def bounce(self):
        return randint(0, 4) == 0

    def draw(self, painter):
        painter.filled_rect(self.bounding_box, self.colour)


BLOCK_GAP = 5
BLOCK_COLUMNS = 10
BLOCK_HEIGHT = 14
BLOCK_COLOURS = [
    (34, 67, 83),
    (34, 67, 83),
    (64, 67, 83),
    (94, 67, 83),
    (124, 67, 83),
    (154, 67, 83),
    (184, 67, 83),
    (214, 67, 83),
    (244, 67, 83),
    (244, 67, 83),
]
BLOCK_AREA_WIDTH = WIDTH - (2 * MARGIN_WIDTH) - (2 * BORDER_WIDTH) - BLOCK_GAP
BLOCK_AREA_LEFT = MARGIN_WIDTH + BORDER_WIDTH + BLOCK_GAP
BLOCK_AREA_TOP = HEADER_HEIGHT + BORDER_WIDTH + BLOCK_GAP
BLOCK_AND_GAP_WIDTH = BLOCK_AREA_WIDTH / BLOCK_COLUMNS
BLOCK_WIDTH = BLOCK_AND_GAP_WIDTH - BLOCK_GAP
BLOCK_AND_GAP_HEIGHT = BLOCK_HEIGHT + BLOCK_GAP

block_rects = []


def setup_block_rects():
    global block_rects

    for x in range(BLOCK_COLUMNS):
        block_rects.append([])
        for y in range(len(BLOCK_COLOURS)):
            left = BLOCK_AREA_LEFT + (BLOCK_AND_GAP_WIDTH * x)
            top = BLOCK_AREA_TOP + (BLOCK_AND_GAP_HEIGHT * y)
            rect = Rect(left, top, BLOCK_WIDTH, BLOCK_HEIGHT)
            block_rects[x].append(rect)


blocks = []


def setup_blocks():
    global blocks
    blocks = []

    for x in range(len(block_rects)):
        for y in range(len(block_rects[x])):
            rect = block_rects[x][y]
            colour = BLOCK_COLOURS[y]
            blocks.append(Block(rect, colour, 10 - y))


setup_block_rects()
setup_blocks()

pgzrun.go()
