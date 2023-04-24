import pygame as pg
import time

pg.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 1000

window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class GameObject:
    def __init__(self, img, x, y, speed):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


class Bullet(GameObject):
    def __init__(self, img, x, y, speed, direction, owner):
        super().__init__(img, x, y, speed)
        self.direction = direction
        self.owner = owner

    def update(self):
        if self.owner == 1:
            if pg.sprite.collide_rect(self, player2):
                player2.hp -= 1
                bullets.remove(self)

        elif self.owner == 2:
            if pg.sprite.collide_rect(self, player1):
                player1.hp -= 1
                bullets.remove(self)

        if self.direction == 'left' and self.rect.x > 0:
            self.rect.x -= self.speed
        elif self.direction == 'right' and self.rect.x < WIN_WIDTH:
            self.rect.x += self.speed
        elif self.direction == 'up' and self.rect.y < WIN_HEIGHT:
            self.rect.y -= self.speed
        elif self.direction == 'down' and self.rect.y > 0:
            self.rect.y += self.speed

        window.blit(self.img, (self.rect.x, self.rect.y))


class Player1(GameObject):
    def __init__(self, img, x, y, speed):
        super().__init__(img, x, y, speed)
        self.hp = 10
        self.direct = 'left'
        self.cd = 0

    def update(self):
        if self.hp <= 0:
            return False

        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.direct = 'up'
        if keys[pg.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.direct = 'left'
        if keys[pg.K_s] and self.rect.y+40 < WIN_HEIGHT:
            self.rect.y += self.speed
            self.direct = 'down'
        if keys[pg.K_d] and self.rect.x+30 < WIN_WIDTH:
            self.rect.x += self.speed
            self.direct = 'right'

        if keys[pg.K_q] and time.time() - self.cd >= 0.5:
            self.shoot()
            self.cd = time.time()

        window.blit(self.img, (self.rect.x, self.rect.y))

        return True

    def shoot(self):
        bullet = Bullet(pg.image.load('bullet.png'), self.rect.x, self.rect.y, 5, self.direct, 1)
        bullets.append(bullet)


class Player2(GameObject):
    def __init__(self, img, x, y, speed):
        super().__init__(img, x, y, speed)
        self.hp = 10
        self.direct = 'right'
        self.cd = 0

    def update(self):
        if self.hp <= 0:
            return False

        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.direct = 'up'
        if keys[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.direct = 'left'
        if keys[pg.K_DOWN] and self.rect.y+40 < WIN_HEIGHT:
            self.rect.y += self.speed
            self.direct = 'down'
        if keys[pg.K_RIGHT] and self.rect.x+30 < WIN_WIDTH:
            self.rect.x += self.speed
            self.direct = 'right'

        if keys[pg.K_SPACE] and time.time() - self.cd >= 0.5:
            self.shoot()
            self.cd = time.time()

        window.blit(self.img, (self.rect.x, self.rect.y))

        return True

    def shoot(self):
        bullet = Bullet(pg.image.load('bullet.png'), self.rect.x, self.rect.y, 5, self.direct, 2)
        bullets.append(bullet)


FPS = 30
clock = pg.time.Clock()

bullets = []

player1 = Player1(pg.image.load('terrorist.png'), 100, 100, 3)
player2 = Player2(pg.image.load('countert.png'), WIN_WIDTH - 100, WIN_HEIGHT - 100, 3)

font = pg.font.SysFont('Arial', 64)

game = True
while game:
    clock.tick(FPS)

    pg.draw.rect(window, (120, 120, 120), (0, 0, 1000, 1000))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False

    player1_game = player1.update()
    player2_game = player2.update()

    if not player1_game:
        GameOver = font.render('PLAYER 2 - WINNER!!!', True, (255, 0, 0))
        window.blit(GameOver, (WIN_WIDTH//2-200, WIN_HEIGHT//2))
    if not player2_game:
        GameOver = font.render('PLAYER 1 - WINNER!!!', True, (0, 0, 255))
        window.blit(GameOver, (WIN_WIDTH//2-200, WIN_HEIGHT//2))

    pg.draw.rect(window, (255, 0, 0), (0, 0, player1.hp*20, 10))
    pg.draw.rect(window, (0, 0, 255), (WIN_WIDTH-200, 0, player2.hp*20, 10))

    for bul in bullets:
        bul.update()

    pg.display.update()




