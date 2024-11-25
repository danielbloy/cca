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
        # Returns the bounding box of the ball
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

    def draw(self, draw):
        draw.filled_circle(self.position, self.radius, self.colour)

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

draw_funcs.append(ball.draw)
update_funcs.append(ball.update)

playing = False
serving = True
game_over = False


def start_game(dt):
    global score, level, lives, playing, serving, game_over

    if not playing and keyboard.space:
        score = 0
        level = 1
        lives = STARTING_LIVES
        playing = True
        serving = True
        game_over = False
        setup_blocks()


def serve_ball(dt):
    global serving, ball

    if serving:
        # If we are serving, keep the ball with the paddle.
        ball.position = paddle.position

        # If space is pressed, serve the ball
        if keyboard.space:
            serving = False
            ball.serve()


update_funcs.append(start_game)
update_funcs.append(serve_ball)


def draw_serving(draw):
    if serving:
        draw.text(f"Level {level}",
                  center=(WIDTH / 2, HEIGHT / 2),
                  color=SCORE_COLOUR,
                  fontsize=72)
        draw.text("Press space to serve",
                  center=(WIDTH / 2, HEIGHT * 3 / 4),
                  color=SCORE_COLOUR,
                  fontsize=36)


draw_funcs.append(draw_serving)


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

    def draw(self, draw):
        draw.filled_rect(self.bounding_box, self.colour)


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


def draw_blocks(draw):
    for block in blocks:
        block.draw(draw)


draw_funcs.append(draw_blocks)


def check_for_collisions(dt):
    global score, blocks

    if ball.vy > 0 and ball.collide(paddle.bounding_box):
        ball.bounce()

    blocks_to_destroy = [
        block for block in blocks if ball.collide(block.bounding_box)
    ]
    if blocks_to_destroy:
        for block in blocks_to_destroy:
            score += block.value
            blocks.remove(block)
            if block.bounce:
                ball.bounce()


update_funcs.append(check_for_collisions)


def check_for_dropping_the_ball(dt):
    global lives, playing, serving, game_over

    if ball.y > (paddle.y + paddle.height + ball.radius):
        ball.stop()
        serving = True
        lives -= 1
        if lives <= 0:
            game_over = True
            playing = False


update_funcs.append(check_for_dropping_the_ball)


def check_for_new_level(dt):
    global level, lives, playing, serving, blocks

    if playing and len(blocks) == 0:
        level += 1
        lives += 1
        serving = True
        setup_blocks()


update_funcs.append(check_for_new_level)


def draw_game_over(draw):
    if game_over:
        draw.text("GAME OVER",
                  center=(WIDTH / 2, HEIGHT * 5 / 8),
                  color=SCORE_COLOUR,
                  fontsize=72)


draw_funcs.append(draw_game_over)

pgzrun.go()
