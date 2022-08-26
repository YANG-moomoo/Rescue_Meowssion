'''子彈'''

import pygame
import os
import math
from setting import *

bullet_img = pygame.image.load(os.path.join("img/bullet", "PeaNormal_0.png"))
bullet_big_img = pygame.transform.scale(bullet_img, (108, 64))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        c, d = pygame.mouse.get_pos()
        self.image = bullet_big_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        self.rect.centerx = x
        self.rect.centery = y
        distance_A_B = math.sqrt((x - c) ** 2 + (y - d) ** 2)

        unit_vector_x = (x - c) / distance_A_B
        unit_vector_y = (y - d) / distance_A_B

        self.speedx = -unit_vector_x * BULLET_SPEED
        self.speedy = -unit_vector_y * BULLET_SPEED

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        elif self.rect.right < 0:
            self.kill()
        elif self.rect.left > WIDTH:
            self.kill()