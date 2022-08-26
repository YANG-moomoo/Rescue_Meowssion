'''補給品'''

import pygame
import random
import os

BLACK = (0, 0, 0)
HEIGHT = 810

powers = pygame.sprite.Group()
power_imgs = {}
power_imgs['blood'] = pygame.image.load(os.path.join("img/power", "blood_old.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img/power", "gun.png"))

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['blood', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()