import pygame
import os
import time
from setting import WIDTH, HEIGHT, FPS
from tutorial import Tutorial
from buttons import Buttons

pygame.init()
pygame.mixer.init()

start_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"btn-start.png")), (285, 100))
sound_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"sound.png")), (70, 70))
mute_img = pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu", f"mute.png")), (70, 70))
title_anim = [pygame.transform.scale(pygame.image.load(os.path.join("img/start_menu/title", f"title-ani-{i}.png")), (WIDTH, HEIGHT)) for i in range(20)]

class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))

        # button
        self.title_img = None
        self.title_anim = title_anim
        self.animation_index = 0
        self.last_update = time.time()
        self.frame_rate = 0.1
        self.start_img = start_img

        self.start_btn = Buttons(572.5, 650, 295, 110) # x, y, width, height
        self.sound_btn = Buttons(1260, 720, 80, 80)
        self.mute_btn = Buttons(1350, 720, 80, 80)
        #self.buttons = [self.start_btn]

        self.volume = 0.4
        self.sound_img = sound_img
        self.mute_img = mute_img

    def play_music(self):
        pygame.mixer.music.load("audio/meowSSion.mp3")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1, 0)

    def draw(self, surf):
        self.title_img = self.title_anim[self.animation_index]
        surf.blit(self.title_img, (0, 0))
        surf.blit(self.start_img, (WIDTH // 2 - 142.5, 650)) #
        surf.blit(self.sound_img, (WIDTH - 175, 720))
        surf.blit(self.mute_img, (WIDTH - 85, 720))

    def update_animation(self):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.animation_index += 1
            if self.animation_index < len(self.title_anim) - 1:
                self.title_img = self.title_anim[self.animation_index]
            else:
                self.title_img = self.title_anim[self.animation_index]
                self.animation_index = 0

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("貓貓救援大作戰")
        self.play_music()

        while run:
            clock.tick(FPS)
            self.update_animation()
            self.draw(self.menu_win)
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound_btn.clicked(x, y):
                        pygame.mixer.music.unpause()

                    if self.mute_btn.clicked(x, y):
                        pygame.mixer.music.pause()

                    if self.start_btn.clicked(x, y):
                       ttl = Tutorial()
                       ttl.ttl_run()
                       run = False

            pygame.display.update()
        pygame.quit()