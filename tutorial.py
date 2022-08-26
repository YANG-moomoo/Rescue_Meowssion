import pygame
import os
import time
from setting import WIDTH, HEIGHT, FPS
from game import Game

ttl_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/tutorial", f"ttl-{i+1}.png")), (WIDTH, HEIGHT)) for i in range(5)]

names = locals()
fire_img = []

for i in range(0, 6):
    names['fire_image%s' % i] = pygame.transform.scale(pygame.image.load("img/fire/fire_%s.png" % i), (105, 85))
    fire_img.append(names['fire_image%s' % i])

player_img = pygame.transform.scale(pygame.image.load("img/player/run-2.png"), (130, 130))

class Tutorial:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.page = 1
        self.page_min = 1
        self.page_max = 5

        self.fire_num = 0
        self.fire_image = fire_img[self.fire_num]
        self.last_update = time.time()
        self.frame_rate = 0.1

    def draw(self, page, surf):
        surf.blit(ttl_list[page - 1], (0, 0))

    def draw2(self, page, surf):
        surf.blit(player_img, (900, 350))

    def fire_ani(self, surf):
        now = time.time()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.fire_num += 1
            if self.fire_num < len(fire_img) - 1:
                self.fire_image = fire_img[self.fire_num]
            else:
                self.fire_image = fire_img[self.fire_num]
                self.fire_num = 0

        surf.blit(self.fire_image, (840, 500))
        surf.blit(self.fire_image, (930, 500))

    def ttl_run(self):
        pygame.init()

        run = True
        clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(0.1)

        while run:
            clock.tick(FPS)

            self.draw(self.page, self.menu_win)
            if self.page == 1:
                self.fire_ani(self.menu_win)
            elif self.page == 3:
                self.draw2(self.page, self.menu_win)

            # x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if self.page == self.page_max:
                        game = Game()
                        game.game_run()
                        run = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if not self.page == self.page_max:
                            self.page += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.page == self.page_min:
                            self.page = 1
                        else:
                            self.page -= 1
                    elif event.key == pygame.K_s:
                        game = Game()
                        game.game_run()
                        run = False

            pygame.display.update()