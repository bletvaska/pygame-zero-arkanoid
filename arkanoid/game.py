#!/usr/bin/env pgzrun
WIDTH=640
HEIGHT=480
TITLE='arkanoid.py'

ball = Actor('ball')
#ball.x = WIDTH / 2
#ball.y = HEIGHT / 2
ball.pos = (WIDTH / 2, HEIGHT / 2)

def update():
    ball.x = ball.x + 1
    ball.y = ball.y - 1


def draw():
    screen.clear()
    ball.draw()

