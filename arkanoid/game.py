#!/usr/bin/env pgzrun
from random import choice

WIDTH = 640
HEIGHT = 480
TITLE = "arkanoid.py"


class Brick(Actor):
    def __init__(self, color="purple", lives=1):
        super().__init__(f"brick.{color}")  # Actor('brick.purple')
        self.lives = lives

    def update(self):
        # collision detection brick with ball
        if self.colliderect(ball):
            ball.dy *= -1
            ball.score += 10
            self.lives -= 1
            if self.lives <= 0:
                bricks.remove(self)


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


colors = ("red", "grey", "purple", "blue", "green")
bricks = []
for row in range(5):
    for col in range(10):
        brick = Brick(choice(colors), lives=3)
        brick.left = col * brick.width
        brick.top = row * brick.height + brick.height  # 32
        bricks.append(brick)


def update():
    ball.update()
    paddle.update()

    # god mode
    paddle.x = ball.x

    # ukoncenie hry, ked lopticka preleti cez dolny okraj obrazovky
    if ball.bottom >= HEIGHT:
        print("Game Over")
        quit()

    # check if there are any bricks left
    if len(bricks) == 0:
        print("Well done")
        quit()

    # update all the bricks
    for brick in bricks:
        brick.update()


background1 = Actor("background2")
background2 = Actor("background2")
background2.left = background1.right


def draw():
    # screen.blit('background', (0, 0))
    background1.draw()
    background2.draw()

    background1.x -= 1
    background2.x -= 1

    if background1.right == 0:
        background1.left = background2.right
    elif background2.right == 0:
        background2.left = background1.right

    ball.draw()
    paddle.draw()

    for brick in bricks:
        brick.draw()

    # print score
    screen.draw.text(f"Score: {ball.score:06}", topright=(WIDTH - 10, 10))
