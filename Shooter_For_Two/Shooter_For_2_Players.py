import pygame as pg
import time
import random

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
    def __init__(self, img, x, y, speed, mouse_pos):
        super().__init__(img, x, y, speed)
        self.mouse_pos = mouse_pos
        self.py = player1.rect.y
        self.px = player1.rect.x

        self.mx = self.mouse_pos[0]
        self.my = self.mouse_pos[1]

        if self.mx > self.px:
            self.xdiff = self.mx - self.px
            self.dirx = True
        elif self.mx < self.px:
            self.xdiff = self.px - self.mx
            self.dirx = False
        else:
            self.xdiff = 100
            self.dirx = True

        if self.my > self.py:
            self.ydiff = self.my - self.py
            self.diry = True
        elif self.my < self.py:
            self.ydiff = self.py - self.my
            self.diry = False
        else:
            self.ydiff = 100
            self.diry = True

        self.speedx = self.speed / (1 + (self.ydiff/self.xdiff))
        self.speedy = self.speed - self.speedx

    def update(self):
        for enemy in enemies:
            if pg.sprite.collide_rect(self, enemy):
                if self in bullets:
                    bullets.remove(self)
                if enemy in enemies:
                    enemies.remove(enemy)

        if self.dirx:
            self.rect.x += self.speedx
            if self.diry:
                self.rect.y += self.speedy
            else:
                self.rect.y -= self.speedy
        else:
            self.rect.x -= self.speedx
            if self.diry:
                self.rect.y += self.speedy
            else:
                self.rect.y -= self.speedy

        '''
        if self.direction == 'left' and self.rect.x > 0:
            self.rect.x -= self.speed
        elif self.direction == 'right' and self.rect.x < WIN_WIDTH:
            self.rect.x += self.speed
        elif self.direction == 'up' and self.rect.y < WIN_HEIGHT:
            self.rect.y -= self.speed
        elif self.direction == 'down' and self.rect.y > 0:
            self.rect.y += self.speed
        '''

        window.blit(self.img, (self.rect.x, self.rect.y))


class Enemy(GameObject):
    def __init__(self, img, x, y, speed):
        super().__init__(img, x, y, speed)

    def update(self):
        if pg.sprite.collide_rect(self, player1):
            enemies.remove(self)
            player1.hp -= 1

        flagx = True
        flagy = True

        ydiff = 0
        xdiff = 0

        if self.rect.x > player1.rect.x:
            xdiff = self.rect.x - player1.rect.x
            dirx = False
        elif self.rect.x < player1.rect.x:
            xdiff = player1.rect.x - self.rect.x
            dirx = True
        else:
            dirx = True
            speedx = 0
            flagx = False

        if self.rect.y > player1.rect.y:
            ydiff = self.rect.y - player1.rect.y
            diry = False
        elif self.rect.y < player1.rect.y:
            ydiff = player1.rect.y - self.rect.y
            diry = True
        else:
            speedy = 0
            diry = True
            flagy = False

        if flagx:
            speedx = self.speed / (1 + (ydiff / xdiff))
        if flagy:
            speedy = self.speed - speedx

        if dirx and self.rect.x + speedx < WIN_WIDTH:
            self.rect.x += speedx
            if diry and self.rect.y + speedx < WIN_HEIGHT:
                self.rect.y += speedy
            elif not diry and self.rect.y - speedy > 0:
                self.rect.y -= speedy
        elif not dirx and self.rect.x - speedx > 0:
            self.rect.x -= speedx
            if diry and self.rect.y + speedy < WIN_HEIGHT:
                self.rect.y += speedy
            elif not diry and self.rect.y - speedy > 0:
                self.rect.y -= speedy

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

        if keys[pg.K_q] and time.time() - self.cd >= 0.1:
            self.shoot()
            self.cd = time.time()

        window.blit(self.img, (self.rect.x, self.rect.y))

        return True

    def shoot(self):
        bullet = Bullet(pg.image.load('bullet.png'), self.rect.x, self.rect.y, 5, pg.mouse.get_pos())
        bullets.append(bullet)


FPS = 30
clock = pg.time.Clock()

enemies = []
bullets = []

player1 = Player1(pg.image.load('terrorist.png'), 100, 100, 3)

font = pg.font.SysFont('Arial', 64)

game = True
while game:
    clock.tick(FPS)

    pg.draw.rect(window, (120, 120, 120), (0, 0, 1000, 1000))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False

    player1_game = player1.update()

    for i in range(15-len(enemies)):
        enemy = Enemy(pg.image.load('enemy.png'), random.randint(50, 950), random.randint(50, 950), 3)
        enemies.append(enemy)

    pg.draw.rect(window, (255, 0, 0), (0, 0, player1.hp*20, 10))

    for enemy in enemies:
        enemy.update()

    for bul in bullets:
        bul.update()

    pg.display.update()




