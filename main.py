# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time

import pygame.display
from pygame.sprite import Sprite

WIDTH = 1024
HIGHT = 768
FILL_COLOR = pygame.Color(0, 0, 0)
ENEMY_TANK_NUM = 12
ENEMY_TANK_INIT_TOP = 50
# 敌方坦克移动多少步后就改变方向
ENEMY_TANK_STEP = 60
TANK_SPEED = 5
BULLET_SPEED = 10


class MainGame:
    window = None
    myTank = None
    myBulletList = []
    enemyTankList = []
    enemyBulletList = []

    def __init__(self):
        pass

    def start(self):
        # 加载主窗口
        Music('start').play()
        pygame.display.init()
        pygame.display.set_caption("坦克大战v1.01")
        # 设置窗口大小
        MainGame.window = pygame.display.set_mode([WIDTH, HIGHT])
        MainGame.myTank = Tank(int(WIDTH / 2), int(HIGHT / 2))
        # 创建敌方坦克
        self.createEnemyTank()
        # 主窗口一直显示
        while True:
            time.sleep(0.03)
            self.getEvents()
            # 添加窗口填充色，否则坦克移动会留残影
            MainGame.window.fill(FILL_COLOR)
            if MainGame.myTank.isLive:
                MainGame.myTank.display()
            else:
                # pygame.font.init()
                # font = pygame.font.SysFont('kaiti', 60)
                # text_gameover = font.render('GAME OVER', True, pygame.Color(255, 0, 0))
                # rect = MainGame.window.get_rect()
                # rect.left = rect.width / 2
                # rect.top = rect.height / 2
                # MainGame.window.blit(text_gameover, rect)
                pass

            # 显示敌方坦克
            self.displayEnemyTanks()
            self.displayBullets()
            # 获取子弹与敌方坦克是否碰撞
            self.getCollide()
            if not MainGame.myTank.isStop:
                MainGame.myTank.move()

            pygame.display.update()

    def end(self):
        pygame.display.quit()
        exit()

    def createEnemyTank(self):
        for i in range(ENEMY_TANK_NUM):
            enemyTank = EnemyTank()
            MainGame.enemyTankList.append(enemyTank)

    def getEvents(self):
        eventList = pygame.event.get()
        # 判断事件
        for event in eventList:
            if event.type == pygame.QUIT:
                self.end()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # print("left")
                    MainGame.myTank.direction = 'L'
                elif event.key == pygame.K_RIGHT:
                    # print("right")
                    MainGame.myTank.direction = 'R'
                elif event.key == pygame.K_UP:
                    # print("up")
                    MainGame.myTank.direction = 'U'
                elif event.key == pygame.K_DOWN:
                    # print("down")
                    MainGame.myTank.direction = 'D'
                elif event.key == pygame.K_SPACE:
                    print('我方发射子弹')
                    if MainGame.myTank.live_bullet < 3:
                        mybullet = Bullet(MainGame.myTank)
                        mybullet.tank.live_bullet += 1
                        MainGame.myBulletList.append(mybullet)
                        Music('shoot').play()

                if not event.key == pygame.K_SPACE:
                    MainGame.myTank.isStop = False
                if event.key == pygame.K_ESCAPE:
                    MainGame.myTank.isLive = True
            elif event.type == pygame.KEYUP:
                if event.key != pygame.K_SPACE:
                    MainGame.myTank.isStop = True

    def getCollide(self):
        # 判断我方子弹是否打中敌方坦克
        for myBullet in MainGame.myBulletList:
            for enemyTank in MainGame.enemyTankList:
                if pygame.sprite.collide_rect(enemyTank, myBullet):
                    myBullet.isLive = False
                    enemyTank.isLive = False
                    explode = Explode(enemyTank)
                    explode.display()
                    Music('explode').play()
        # 判断敌方子弹是否打中我方坦克
        for enemyBullet in MainGame.enemyBulletList:
            if pygame.sprite.collide_rect(enemyBullet, MainGame.myTank):
                enemyBullet.isLive = False
                MainGame.myTank.isLive = False
                explode = Explode(MainGame.myTank)
                explode.display()
                Music('explode').play()

    def displayBullets(self):
        for mybullet in MainGame.myBulletList:
            if mybullet.isLive:
                mybullet.display()
                mybullet.move()

            else:
                MainGame.myBulletList.remove(mybullet)
                mybullet.tank.live_bullet -= 1
        for enemybullet in MainGame.enemyBulletList:
            if enemybullet.isLive:
                enemybullet.display()
                enemybullet.move()
            else:
                MainGame.enemyBulletList.remove(enemybullet)
                enemybullet.tank.live_bullet -= 1

    def displayEnemyTanks(self):
        for enemyTank in MainGame.enemyTankList:
            if enemyTank.isLive:
                enemyTank.display()
                enemyTank.move()
            else:
                MainGame.enemyTankList.remove(enemyTank)


class BaseSprite(Sprite):
    def __init__(self):
        super(BaseSprite, self).__init__()


class Tank(BaseSprite):
    def __init__(self, left=None, top=None):
        self.imgs = {'U': pygame.image.load('imgs/1.gif'),
                     'D': pygame.image.load('imgs/2.gif'),
                     'L': pygame.image.load('imgs/3.gif'),
                     'R': pygame.image.load('imgs/4.gif')}
        self.direction = 'U'
        self.img = self.imgs[self.direction]
        self.rect = self.img.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = TANK_SPEED
        self.isStop = True
        self.live_bullet = 0
        self.isLive = True

    def move(self):

        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            # print(f'self.rect.top={self.rect.top};win_rect.left+WIDTH={win_rect.top + HIGHT}')
            if self.rect.top + self.rect.height / 2 < HIGHT:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            # print(f'self.rect.left={self.rect.left};win_rect.left+WIDTH={win_rect.left+WIDTH}')
            if self.rect.left + self.rect.width / 2 < WIDTH:
                self.rect.left += self.speed
        # Music('move').play()

    def shoot(self):
        pass

    def display(self):
        self.img = self.imgs[self.direction]
        MainGame.window.blit(self.img, self.rect)


class EnemyTank(Tank):
    def __init__(self):
        self.imgs = {'U': pygame.image.load('imgs/11.gif'),
                     'D': pygame.image.load('imgs/12.gif'),
                     'L': pygame.image.load('imgs/13.gif'),
                     'R': pygame.image.load('imgs/14.gif')}
        self.direction = self.randomDirection()
        self.img = self.imgs[self.direction]
        self.rect = self.img.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = ENEMY_TANK_INIT_TOP
        self.speed = TANK_SPEED
        self.live_bullet = 0
        self.isLive = True

    def move(self):
        if self.discoverEnemy():
            print('敌方发射子弹')
            self.shoot()
        elif self.step > ENEMY_TANK_STEP:
            self.direction = self.randomDirection()

        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
                self.step += 1
            else:
                self.direction = self.randomDirection()
        elif self.direction == 'D':
            # print(f'self.rect.top={self.rect.top};win_rect.left+WIDTH={win_rect.top + HIGHT}')
            if self.rect.top + self.rect.height / 2 < HIGHT:
                self.rect.top += self.speed
                self.step += 1
            else:
                self.direction = self.randomDirection()
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
                self.step += 1
            else:
                self.direction = self.randomDirection()
        elif self.direction == 'R':
            # print(f'self.rect.left={self.rect.left};win_rect.left+WIDTH={win_rect.left+WIDTH}')
            if self.rect.left + self.rect.width / 2 < WIDTH:
                self.rect.left += self.speed
                self.step += 1
            else:
                self.direction = self.randomDirection()

    def randomDirection(self):
        directions = ['U', 'D', 'L', 'R']
        self.step = 0
        return directions[random.randint(0, 3)]

    def shoot(self):
        if self.live_bullet < 1:
            bullet = Bullet(self)
            self.live_bullet += 1
            MainGame.enemyBulletList.append(bullet)

    def discoverEnemy(self):
        isShoot = False
        if self.direction == 'U':
            if MainGame.myTank.rect.top < self.rect.top and MainGame.myTank.rect.left > self.rect.left and MainGame.myTank.rect.left < self.rect.left + self.rect.width:
                isShoot = True
        elif self.direction == 'D':
            if MainGame.myTank.rect.top > self.rect.top and MainGame.myTank.rect.left > self.rect.left and MainGame.myTank.rect.left < self.rect.left + self.rect.width:
                isShoot = True
        elif self.direction == 'L':
            if MainGame.myTank.rect.left < self.rect.left and MainGame.myTank.rect.top > self.rect.top and MainGame.myTank.rect.top < self.rect.top + self.rect.height:
                isShoot = True
        elif self.direction == 'R':
            if MainGame.myTank.rect.left > self.rect.left and MainGame.myTank.rect.top > self.rect.top and MainGame.myTank.rect.top < self.rect.top + self.rect.height:
                isShoot = True
        return isShoot


class Bullet(BaseSprite):
    def __init__(self, tank=None):
        self.img = pygame.image.load('imgs/bullet.gif')
        self.direction = tank.direction
        self.speed = BULLET_SPEED
        self.isLive = True
        self.tank = tank
        self.rect = self.img.get_rect()
        if self.direction == 'U':
            self.rect.top = tank.rect.top - self.rect.height
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'D':
            self.rect.top = tank.rect.top + tank.rect.height
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'L':
            self.rect.top = tank.rect.top + tank.rect.height / 2 + self.rect.height / 2
            self.rect.left = tank.rect.left - self.rect.width
        elif self.direction == 'R':
            self.rect.top = tank.rect.top + tank.rect.height / 2 + self.rect.height / 2
            self.rect.left = tank.rect.left + tank.rect.width

    def move(self):

        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.isLive = False
        elif self.direction == 'D':
            # print(f'self.rect.top={self.rect.top};WIDTH={HIGHT}')
            if self.rect.top + self.rect.height < HIGHT:
                self.rect.top += self.speed
            else:
                self.isLive = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.isLive = False
        elif self.direction == 'R':
            # print(f'self.rect.left={self.rect.left};WIDTH={WIDTH}')
            if self.rect.left + self.rect.width < WIDTH:
                self.rect.left += self.speed
            else:
                self.isLive = False

    def display(self):
        MainGame.window.blit(self.img, self.rect)


class Explode():
    def __init__(self, tank):
        self.tank = tank
        self.img = pygame.image.load('imgs/explod.png')
        self.rect = self.img.get_rect()
        self.rect.top = tank.rect.top
        self.rect.left = tank.rect.left

    def display(self):
        MainGame.window.blit(self.img, self.rect)


class Music():
    def __init__(self, musicname):
        pygame.mixer.init()
        pygame.mixer.music.load(f'imgs/{musicname}.mp3')

    def play(self):
        pygame.mixer.music.play()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Tank')
    MainGame().start()
