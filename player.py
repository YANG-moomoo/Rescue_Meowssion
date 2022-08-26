'''貓貓 (主角)'''

import pygame
from bullet import Bullet
from waterball import Waterball
from soundset import play_sound
from setting import WIDTH, HEIGHT, BLACK
from building import all_sprites

names = locals()
player_img = []
for i in range(1, 9):
    names['cat_image%s' % i] = pygame.transform.scale(pygame.image.load("img/player/run-%s.png" % i), (150, 150))
    player_img.append(names['cat_image%s' % i])

bullets = pygame.sprite.Group()
waterballs = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # 精靈
        self.num = 0
        self.image = player_img[self.num]
        self.image.set_colorkey(BLACK)
        # self.image.set_colorkey(WHITE) # 透明度
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.centerx = 100
        self.rect.bottom = HEIGHT - 30
        self.speedx = 8
        self.vel_y = 0
        self.health = 100
        self.gun = 1
        self.gun_time = 0
        self.count = 0

        self.jump_counter = 0
        self.jumped = False

        self.p_range = 150
        self.p_trans = 90
        self.protected = True

        self.k_range = 100
        self.k_range_max = 1000

    def draw_protect(self, surf):
        surface = pygame.Surface((self.p_range * 2, self.p_range * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (70, 70, 255, self.p_trans), (self.p_range, self.p_range), self.p_range)
        surf.blit(surface, (self.rect.x - self.p_range // 2, self.rect.y - self.p_range // 2))

    def draw_kill_all(self, surf):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 140), (WIDTH // 2, HEIGHT // 2), self.k_range)
        surf.blit(surface, (0, 0))
        if self.k_range < self.k_range_max:
            self.k_range += 60
        elif self.k_range == self.k_range_max:
            self.k_range = 100

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun == 2 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        key_pressed = pygame.key.get_pressed()

        if self.rect.bottom == (HEIGHT - 30):
            self.jump_counter = 0

        # 二段跳
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_SPACE]:
            if (not self.jumped) and 550 < self.rect.bottom <= (HEIGHT - 30):
                if self.jump_counter < 2:
                    self.vel_y = -22
                    play_sound("sfx\smb_jump-small.wav")
                    self.jump_counter += 1
                self.jumped = True

        if not key_pressed[pygame.K_SPACE] and not key_pressed[pygame.K_w]:
            self.jumped = False

        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        self.vel_y += 0.8
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT - 30:
            self.rect.bottom = HEIGHT - 30
        if self.rect.top < 0:
            self.rect.top = 0

        self.count += 1
        if self.count % 10 == 0:
            self.count = 0
            self.num += 1
            if self.num % 8 == 0:
                self.num = 0
            self.image = player_img[self.num]

    # 射子彈
    def shoot(self):
        play_sound("sfx\smb_fireball.wav")
        if self.gun == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        elif self.gun >= 2:
            bullet1 = Bullet(self.rect.centerx, self.rect.top)
            bullet2 = Bullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)

    # 射水球
    def shootwater(self):
        waterball = Waterball(self.rect.left, self.rect.centery)
        play_sound("sfx\smw_swimming.wav")
        all_sprites.add(waterball)
        waterballs.add(waterball)

    # 武器升級成雙彈
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()