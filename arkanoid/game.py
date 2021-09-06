#!/usr/bin/env pgzrun
from random import choice
import logging
from pathlib import Path

from pgzero.actor import Actor
from pgzero.keyboard import keyboard
import pgzrun
import pytmx

WIDTH = 640
HEIGHT = 480
TITLE = "arkanoid.py"


# logger = logging.getLogger('arkanoid')

def get_actor_by_type(actors: list, cls: type):
    for actor in actors:
        if type(actor) == cls:
            return actor

    return None


class Brick(Actor):
    def __init__(self, color="purple", lives=1):
        try:
            super().__init__(f"brick.{color}")  # Actor('brick.purple')
            self.lives = lives
        except KeyError:
            # toto sa nikdy nezrube  # NENECHAVAT PRAZDNY except BLOK!!!!!
            logging.critical(f'File "brick.{color}.png" not found. Please, reinstall game.')
            quit(1)

    def update(self):
        # collision detection brick with ball
        ball = get_actor_by_type(actors, Ball)
        if self.colliderect(ball):
            ball.dy *= -1
            ball.score += 10
            self.lives -= 1
            if self.lives <= 0:
                actors.remove(self)


class Ball(Actor):
    def __init__(self):
        super().__init__("ball")  # Actor('ball')
        self.dx = -1
        self.dy = -1
        self.speed = 5
        self.pos = (WIDTH / 2, HEIGHT / 2)
        self.score = 0

    def update(self):
        self.x = self.x + self.speed * self.dx
        self.y = self.y + self.speed * self.dy

        # odrazenie zhora
        if self.top <= 0:
            self.dy *= -1
            self.top = 0

        # odrazenie zprava
        if self.right >= WIDTH:
            self.dx *= -1
            self.right = WIDTH

        # odrazenie zlava
        if self.left <= 0:
            self.dx *= -1
            self.left = 0

        # odrazenie zdola
        if self.bottom >= HEIGHT:
            self.dy *= -1
            self.bottom = HEIGHT

        # collision detection with paddle
        paddle = get_actor_by_type(actors, Paddle)
        if self.colliderect(paddle):
            print("collision detected")
            self.dy *= -1
            self.bottom = paddle.top


class Paddle(Actor):
    def __init__(self):
        super().__init__("paddle")  # Actor('paddle')
        self.bottom = HEIGHT
        self.x = WIDTH / 2
        self.speed = 7
        self.dx = 0

    def update(self):
        if keyboard.left == True:
            self.dx = -1
        elif keyboard.right == True:
            self.dx = 1
        else:
            self.dx = 0

        self.x = self.x + self.dx * self.speed

        if self.left <= 0:
            self.left = 0

        if self.right >= WIDTH:
            self.right = WIDTH


def update():
    # god mode
    paddle = get_actor_by_type(actors, Paddle)
    ball = get_actor_by_type(actors, Ball)

    # paddle.x = ball.x

    background.x += paddle.dx

    # ukoncenie hry, ked lopticka preleti cez dolny okraj obrazovky
    if ball.bottom >= HEIGHT:
        print("Game Over")
        quit()

    # check if there are any bricks left
    if get_actor_by_type(actors, Brick) is None:
        print("Well done")
        quit()

    # update all the bricks
    for actor in actors:
        actor.update()


def draw():
    background.draw()

    # draw all actors
    for actor in actors:
        actor.draw()

    # print score
    ball = get_actor_by_type(actors, Ball)
    screen.draw.text(f"Score: {ball.score:06}", topright=(WIDTH - 10, 10))


def init_game():
    paddle = Paddle()
    actors.append(paddle)
    actors.append(Ball())

    level = pytmx.TiledMap('maps/level1.tmx')
    layer = level.get_layer_by_name('actors')

    for actor in layer:
        brick = Brick(actor.properties['color'], actor.properties['lives'])
        brick.topleft = (actor.x, actor.y)
        actors.append(brick)

    # extract background image
    bglayer = level.get_layer_by_name('background')
    image = Path(bglayer.image[0])

    global background
    background = Actor(image.stem)
    background.x = paddle.x

background = None
actors = []

init_game()
pgzrun.go()

