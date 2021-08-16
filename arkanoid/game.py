#!/usr/bin/env pgzrun
WIDTH = 640
HEIGHT = 480
TITLE = "arkanoid.py"

class Brick(Actor):
    def __init__(self, color='purple'):
        super().__init__(f'brick.{color}')  # Actor('brick.purple')


def hello():
    print('hello world')


class Ball(Actor):
    def __init__(self):
        super().__init__('ball')  # Actor('ball')
        self.dx = -1
        self.dy = -1
        self.speed = 5
        self.pos = (WIDTH / 2, HEIGHT / 2)

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
        if self.colliderect(paddle):
            print("collision detected")
            self.dy *= -1
            self.bottom = paddle.top

        # collision detection brick with ball
        for brick in bricks:
            if self.colliderect(brick):
                self.dy *= -1
                bricks.remove(brick)
                break


class Paddle(Actor):
    def __init__(self):
        super().__init__('paddle')  # Actor('paddle')
        self.bottom = HEIGHT
        self.x = WIDTH / 2
        self.speed = 7

    def update(self):
        # left arrow pressed
        if keyboard.left == True:
            self.x = self.x - self.speed
            if self.left <= 0:
                self.left = 0

        if keyboard.right == True:
            self.x += self.speed
            if self.right >= WIDTH:
                self.right = WIDTH


ball = Ball()
paddle = Paddle()


bricks = []
for row, color in enumerate(('red', 'grey', 'purple', 'blue', 'green')):
    for col in range(10):
        brick = Brick(color)
        brick.left = col * brick.width
        brick.top = row * brick.height
        bricks.append(brick)


def update():
    ball.update()
    paddle.update()

    # god mode
    paddle.x = ball.x

    # ukoncenie hry, ked lopticka preleti cez dolny okraj obrazovky
    if ball.bottom >= HEIGHT:
        print('Game Over')
        quit()

    # check if there are any bricks left
    if len(bricks) == 0:
        print('Well done')
        quit()


def draw():
    screen.blit('background', (0, 0))
    ball.draw()
    paddle.draw()

    for brick in bricks:
        brick.draw()
