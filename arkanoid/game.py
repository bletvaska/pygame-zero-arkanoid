#!/usr/bin/env pgzrun
WIDTH = 640
HEIGHT = 480
TITLE = "arkanoid.py"

ball = Actor("ball")
# ball.x = WIDTH / 2
# ball.y = HEIGHT / 2
ball.pos = (WIDTH / 2, HEIGHT / 2)
ball.dx = 1
ball.dy = -1
ball.speed = 5

paddle = Actor("paddle")
paddle.bottom = HEIGHT
paddle.x = WIDTH / 2
paddle.speed = 7

bricks = []
for col in range(10):
    for row in range(5):
        brick = Actor("brick.red")
        brick.left = col * brick.width
        brick.top = row * brick.height
        bricks.append(brick)


def update():
    ball.x = ball.x + ball.speed * ball.dx
    ball.y = ball.y + ball.speed * ball.dy

    # odrazenie zhora
    if ball.top <= 0:
        ball.dy *= -1
        ball.top = 0

    # odrazenie zprava
    if ball.right >= WIDTH:
        ball.dx *= -1
        ball.right = WIDTH

    # odrazenie zdola
    if ball.bottom >= HEIGHT:
        ball.dy *= -1
        ball.bottom = HEIGHT

    # odrazenie zlava
    if ball.left <= 0:
        ball.dx *= -1
        ball.left = 0

    # left arrow pressed
    if keyboard.left == True:
        paddle.x = paddle.x - paddle.speed
        if paddle.left <= 0:
            paddle.left = 0

    if keyboard.right == True:
        paddle.x += paddle.speed
        if paddle.right >= WIDTH:
            paddle.right = WIDTH

    # collision detection
    if paddle.colliderect(ball):
        print("collision detected")
        ball.dy *= -1
        ball.bottom = paddle.top

    # collision detection brick with ball
    for brick in bricks:
        if brick.colliderect(ball):
            ball.dy *= -1
            bricks.remove(brick)
            break

    # check if there are any bricks left
    if len(bricks) == 0:
        print('Well done')
        quit()


def draw():
    screen.clear()
    ball.draw()
    paddle.draw()

    for brick in bricks:
        brick.draw()
