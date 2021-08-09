#!/usr/bin/env pgzrun
WIDTH=640
HEIGHT=480
TITLE='arkanoid.py'

ball = Actor('ball')
#ball.x = WIDTH / 2
#ball.y = HEIGHT / 2
ball.pos = (WIDTH / 2, HEIGHT / 2)
ball.dx = 1
ball.dy = -1

def update():
    ball.x = ball.x + ball.dx
    ball.y = ball.y + ball.dy

    if ball.top <= 0:
        ball.dy *= -1

    if ball.right >= WIDTH:
        ball.dx *= -1


def draw():
    screen.clear()
    ball.draw()

