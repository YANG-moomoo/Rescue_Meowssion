'''在地上的火'''

import pygame
import random

from player import all_sprites
from setting import *

names = locals()
fire_img = []

for i in range(0, 6):
    names['fire_image%s' % i] = pygame.transform.scale(pygame.image.load("img/fire/fire_%s.png" % i),(140,112))
    fire_img.append(names['fire_image%s' % i])
fires = pygame.sprite.Group()

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.num = 0
        self.image = fire_img[self.num]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH + 100, WIDTH + 800)
        self.rect.bottom = HEIGHT - 50
        self.count = 0
        self.speed_fire = SPEED

    def update(self):
        self.rect.move_ip(-self.speed_fire, 0)
        if self.rect.right < 0:
            self.kill()
            new_fire()

        self.count += 1
        if self.count % 8 == 0:
            self.count = 0
            self.num += 1
            if self.num % 6 == 0:
                self.num = 0
            self.image = fire_img[self.num]

#生成新的火
def new_fire():
    f = Fire()
    all_sprites.add(f)
    fires.add(f)