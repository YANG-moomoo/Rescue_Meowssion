'''地板（背景）'''
import pygame
import os
from setting import *

#讀各種圖片檔案
background_img_gray = pygame.image.load(os.path.join("img/ground", "War2.png")).convert()
background_mini_img_1 = pygame.transform.scale(background_img_gray, (1440, 810))

background_img_sun = pygame.image.load(os.path.join("img/ground", "War1_1.png")).convert()
background_mini_img_2 = pygame.transform.scale(background_img_sun, (1440, 810))

background_img_dusk = pygame.image.load(os.path.join("img/ground", "War3_1.png")).convert()
background_mini_img_3 = pygame.transform.scale(background_img_dusk, (1440, 810))

background_img_moon = pygame.image.load(os.path.join("img/ground", "War_4.png")).convert()
background_mini_img_4 = pygame.transform.scale(background_img_moon, (1440, 810))

class Ground:
    def __init__(self):
        # 匯入圖片
        self.image_0 = background_mini_img_2
        self.image_1 = background_mini_img_2
        self.rect_0 = self.image_0.get_rect()
        self.rect_1 = self.image_1.get_rect()
        self.ground_speed = SPEED
        self.rect_0.left = 0
        self.rect_1.left += WIDTH
        self.round = 2

    '''更新地板'''
    def update(self):
        self.rect_0.left -= self.ground_speed
        self.rect_1.left -= self.ground_speed
        if self.rect_0.right < 0:
            self.rect_0.left = self.rect_1.right
        if self.rect_1.right < 0:
            self.rect_1.left = self.rect_0.right

    '''將地板畫到螢幕'''
    def draw(self, screen):
        # 兩張相同ㄉ圖片互相接續輪流出現
        screen.blit(self.image_0, self.rect_0)
        screen.blit(self.image_1, self.rect_1)

    def change_ground(self):
        if self.round == 1:
            self.image_0 = background_mini_img_2
            self.image_1 = background_mini_img_2

        elif self.round == 2:
            self.image_0 = background_mini_img_3
            self.image_1 = background_mini_img_3
        elif self.round == 3:
            self.image_0 = background_mini_img_4
            self.image_1 = background_mini_img_4
        else:
            self.image_0 = background_mini_img_1
            self.image_1 = background_mini_img_1

        if self.round < 4:
            self.round += 1
        else:
            self.round = 1