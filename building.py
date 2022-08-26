'''建築物'''

import pygame
import random
import os
from setting import *

all_sprites = pygame.sprite.Group()
buildings = pygame.sprite.Group()

building_imgs = []
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{0}.png")), (150, 150)))
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{1}.png")), (140, 240)))
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{2}.png")), (100, 240)))
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{3}.png")), (220, 216)))
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{4}.png")), (150, 150)))
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{5}.png")), (150, 150)))
building_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/building", f"building{6}.png")), (160, 240)))

class Building(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(building_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH + 100, WIDTH + 800)
        self.rect.bottom = HEIGHT - 30
        self.speed_build = SPEED

    def build_speedup(self, up):
        self.build_speed += up

    def update(self):
        self.rect.move_ip(-self.speed_build, 0)
        if self.rect.right < 0:
            self.kill()
            new_building()
            
#生成新的建築
def new_building():
    b = Building()
    all_sprites.add(b)
    buildings.add(b)