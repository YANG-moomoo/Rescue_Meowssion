#掉落物
import pygame
import random
import os

from building import all_sprites

WIDTH = 1440
HEIGHT = 810


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

rock_imgs = []
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{0}.png")).convert(), (300, 300)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{1}.png")).convert(), (200, 200)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{2}.png")).convert(), (250, 250)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{3}.png")).convert(), (300, 300)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{4}.png")).convert(), (150, 150)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{5}.png")).convert(), (200, 200)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{6}.png")).convert(), (200, 200)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{7}.png")).convert(), (200, 200)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{8}.png")).convert(), (100, 100)))
rock_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/rock", f"rock{9}.png")).convert(), (120, 120)))

rocks = pygame.sprite.Group()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        # self.image_ori.set_colorkey(WHITE)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    # 旋轉效果
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT  or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

#生成新的石頭
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)