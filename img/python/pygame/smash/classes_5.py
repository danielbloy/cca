from random import randint

from pgzero.rect import Rect
from pgzero.screen import Screen

WIDTH = 640
HEIGHT = 800
GRAVITY = 120

screen: Screen

game_objects = []


def draw():
    screen.fill((0, 0, 0))

    for game_object in game_objects:
        game_object.draw(screen.draw)


def update(dt):
    global game_objects

    choice = randint(1, 30)
    if choice == 1:
        box = Square(100, 100, 10)
        game_objects.append(box)
    elif choice == 2:
        circle = Circle(200, 100, 5)
        game_objects.append(circle)
    elif choice == 3:
        triangle = Triangle(300, 100, 5)
        game_objects.append(triangle)
        
    for game_object in game_objects:
        game_object.update(dt)

    game_objects = [game_object for game_object in game_objects if game_object.alive]


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 5

    @property
    def alive(self):
        return self.lifetime > 0

    def update(self, dt):
        self.lifetime -= dt
        self.y += GRAVITY * dt


class Square(Shape):
    def __init__(self, x, y, width):
        super().__init__(x, y)
        self.colour = (90, 180, 90)
        self.width = width

    def draw(self, draw):
        half_width = self.width / 2
        rect = Rect(self.x - half_width, self.y - half_width, self.width, self.width)
        draw.filled_rect(rect, self.colour)


class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.colour = (3, 50, 90)
        self.radius = radius

    def draw(self, draw):
        draw.filled_circle((self.x, self.y), self.radius, self.colour)

import pgzrun
pgzrun.go()