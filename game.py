import pygame
import random
import os
import time

from rock import Rock, new_rock, rocks, screen
from ground import Ground
from fire import Fire, new_fire, fires
from building import Building, new_building, buildings, all_sprites
from power import Power, powers
from explosion import Explosion
from soundset import play_sound
from setting import *
from buttons import Buttons
from player import Player, bullets, waterballs
from protect import Protect

end_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end", f"end.png")),(285, 100))
again_img = pygame.transform.scale(pygame.image.load(os.path.join("img/end", f"again.png")),(285, 100))
tips_list = [pygame.transform.scale(pygame.image.load(os.path.join("img/end/tips", f"tips-{i}.png")), (WIDTH, HEIGHT)) for i in range(23)]
mouse_img = pygame.transform.scale(pygame.image.load(os.path.join("img", f"mouse.png")),(80, 80))

class Game:
    def __init__(self):
        # 設定字型
        self.font_name = os.path.join("ttf/HanyiSentyPagoda.ttf")

        self.init_moment = time.time()
        self.stop_time = 0
        self.init_time = 0
        self.stop_time_count = 0
        self.update_rate = 0.9
        self.new_time = 0

        self.rand_num = 0
        self.talk_list = ["本喵喘口氣 . . . 喵呼 . . .",
                          "本喵喝口水，休息一下 . . . ",
                          "好累 . . . 突然好想吃罐罐 . . . ",
                          "喵呼 . . . 累得跟貓一樣 . . . ",
                          "呼嚕 . . . 呼嚕 . . . ",
                          "休息是為了吃更多罐罐喵 . . . "]
        self.start = True

        self.speedup = 0
        self.pause = False
        self.running = True
        self.close = False
        self.dead = False
        self.change = True
        self.last_change = time.time()

        self.score = 0
        self.count = 0
        self.power_count = 0

        self.show_ready = True
        self.kill_all = False

        # win
        self.end_win = pygame.display.set_mode((WIDTH, HEIGHT))

        # button
        self.end_img = end_img
        self.again_img = again_img
        self.tips_list = tips_list
        self.rand_num2 = random.randrange(len(self.tips_list))

        self.again_btn = Buttons(95, 580, 295, 110)
        self.end_btn = Buttons(95, 680, 295, 110)  # x, y, width, height

        self.mouse_img = mouse_img
        
    # 顯示文字
    def draw_text(self, surf, color , text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)


    # 滑鼠圖示
    def draw_mouse(self, surf, x, y):
        x -= self.mouse_img.get_width() / 2
        y -= self.mouse_img.get_height() / 2

        surf.blit(self.mouse_img, (x, y))

    # 畫生命值
    def draw_health(self, surf, hp, x, y):
        if hp < 0:
            hp = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 20
        fill = (hp/100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if fill > (80/100)*BAR_LENGTH:
            pygame.draw.rect(surf, GREEN, fill_rect)
        elif (79/100)*BAR_LENGTH > fill > (40/100)*BAR_LENGTH :
            pygame.draw.rect(surf, ORANGE, fill_rect)
        else:
            pygame.draw.rect(surf, RED, fill_rect)

        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_weapon_time(self, surf, t, total_t, x, y):
        if t < 0:
            t = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 20
        colorlist = [(111, 159, 255),
                     (94, 137, 255),
                     (64, 94, 152),
                     (43, 62, 101),
                     (15, 22, 36)]
        fill = (t/total_t) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if fill == BAR_LENGTH:
            pygame.draw.rect(surf, (240, 240, 240), fill_rect)
        elif fill >= (80/100)*BAR_LENGTH:
            pygame.draw.rect(surf, colorlist[0], fill_rect)
        elif (80/100)*BAR_LENGTH > fill >= (60/100)*BAR_LENGTH :
            pygame.draw.rect(surf, colorlist[1], fill_rect)
        elif (60/100)*BAR_LENGTH > fill >= (40/100)*BAR_LENGTH :
            pygame.draw.rect(surf, colorlist[2], fill_rect)
        elif (40/100)*BAR_LENGTH > fill >= (20/100)*BAR_LENGTH :
            pygame.draw.rect(surf, colorlist[3], fill_rect)
        elif (20/100)*BAR_LENGTH > fill:
            pygame.draw.rect(surf, colorlist[4], fill_rect)

        if (20/100)*BAR_LENGTH > fill >= (15/100)*BAR_LENGTH:
            # 提示防護罩即將失效
            pygame.draw.rect(surf, colorlist[4], outline_rect, 2)
        else:
            pygame.draw.rect(surf, WHITE, outline_rect, 2)

    #畫遊戲時間
    def draw_time(self):
        time = self.time - self.new_time
        second = time // 1000
        minute = second // 60
        minute = str(minute).zfill(2)
        second_1 = second % 60
        second_1 = str(second_1).zfill(2)
        my_text = f'{minute}' + ':' + f'{second_1}'
        return my_text

    # 顯示準備時間
    def draw_ready_time(self):
        sec = int((time.time() - self.init_moment) // 1)
        return sec

    # 顯示暫停畫面
    def draw_pause(self, surf, num=0, size_big=80, size_small=40):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, (128, 128, 128, 160), [0, 0, WIDTH, HEIGHT])

        font = pygame.font.Font(self.font_name, size_big)
        text_surf_1 = font.render(self.talk_list[num], True, WHITE)
        text_rect_1 = text_surf_1.get_rect()
        text_rect_1.centerx = WIDTH / 2
        text_rect_1.top = HEIGHT / 2 - 90

        font = pygame.font.Font(self.font_name, size_small)
        text_surf_2 = font.render("按下 p 鍵可繼續遊戲", True, WHITE)
        text_rect_2 = text_surf_2.get_rect()
        text_rect_2.centerx = WIDTH / 2
        text_rect_2.top = HEIGHT / 2 + 60

        if not self.show_ready:
            surf.blit(surface, (0, 0))
            surf.blit(text_surf_1, text_rect_1)
            surf.blit(text_surf_2, text_rect_2)
        else:
            countdown = str(3 - self.draw_ready_time())
            if self.draw_ready_time() >= 3:
                countdown = "GO!"

            font = pygame.font.Font(self.font_name, 400)
            text_surf = font.render(countdown, True, WHITE)
            text_rect = text_surf.get_rect()
            text_rect.centerx = WIDTH / 2 - 20
            text_rect.top = HEIGHT / 2 - 320

            surf.blit(surface, (0, 0))
            surf.blit(text_surf, text_rect)

    # 畫gameover頁面
    def draw_close(self, surf, num = 0):
        font = pygame.font.Font(self.font_name, 60)
        text_surf_1 = font.render("本次挑戰分數", True, RED1)
        text_rect_1 = text_surf_1.get_rect()
        text_rect_1.left = 60
        text_rect_1.top = 380

        font = pygame.font.Font(self.font_name, 60)
        text_surf_2 = font.render("「 " + str(self.score) + " 分 」", True, RED1)
        text_rect_2 = text_surf_2.get_rect()
        text_rect_2.centerx = text_rect_1.centerx
        text_rect_2.top = 480

        surf.blit(self.tips_list[num], (0, 0))
        surf.blit(text_surf_1, text_rect_1)
        surf.blit(text_surf_2, text_rect_2)
        surf.blit(self.again_img, (100, 580))
        surf.blit(self.end_img, (100, 680))

    ground = Ground()

    building = Building()
    player = Player()
    fire = Fire()
    rock = Rock()
    protect = Protect()

    all_sprites.add(player)

    for i in range(3):
        new_rock()
    for i in range(1):
        new_building()
    # for i in range(5):
    #     new_fire()

    # 遊戲迴圈
    def game_run(self):
        pygame.init()

        clock = pygame.time.Clock()

        self.init_time = pygame.time.get_ticks()
        self.running = True

        while self.running:
            clock.tick(FPS)
            while self.close:
                pygame.event.set_grab(False)

                self.rand_num2 = random.randrange(len(self.tips_list))
                x, y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.close = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.end_btn.clicked(x, y):
                            self.running = False
                            self.close = False

                        if self.again_btn.clicked(x, y):
                            self.__init__()
                            self.protect.__init__()
                            self.ground.__init__()
                            self.player.__init__()

                            for g in bullets.sprites():
                                g.kill()
                            for w in waterballs.sprites():
                                w.kill()
                            for p in powers.sprites():
                                p.kill()

                            for f in fires.sprites():
                                f.kill()
                            for b in buildings.sprites():
                                b.kill()
                            for r in rocks.sprites():
                                r.kill()

                            for i in range(3):
                                new_rock()
                            for i in range(1):
                                new_building()

                            self.new_time = pygame.time.get_ticks()

                            self.close = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        
                    if event.key == pygame.K_p:
                        self.rand_num = random.randrange(len(self.talk_list))
                        if self.pause == True:
                            self.stop_time_count += pygame.time.get_ticks() - self.stop_time
                            pygame.mixer.music.unpause()  # 音樂繼續
                        else:
                            play_sound("sfx/smb_pause.wav")
                            self.stop_time = pygame.time.get_ticks()
                            pygame.mixer.music.pause()  # 音樂暫停
                        self.pause = not self.pause

                    '''通殺test'''
                    if event.key == pygame.K_n:
                        self.kill_all = True

                        f_num, r_num = 0, 0
                        for f in fires.sprites():
                            f_num += 1
                            f.kill()
                        for r in rocks.sprites():
                            r_num += 1
                            r.kill()
                        for i in range(f_num):
                            new_fire()
                        for i in range(r_num):
                            new_rock()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.pause:
                        if event.button == 1:
                            self.player.shoot()
                        elif event.button == 3:
                            self.player.shootwater()

            if self.pause:
                pygame.event.set_grab(False)
            else:
                # 滑鼠控制
                x, y = pygame.mouse.get_pos()
                if x < 0:
                    x = 0
                elif y < 0:
                    y = 0
                elif x > WIDTH:
                    x = WIDTH
                elif y > HEIGHT:
                    y = HEIGHT
                pygame.event.set_grab(True)

            # 更新遊戲
            now = pygame.time.get_ticks()
            if self.running and not self.pause:
                self.time = now - self.stop_time_count - self.init_time
                all_sprites.update()
                self.ground.update()
                self.protect.update()

            elif not self.show_ready:
                self.time = self.time
            else:
                self.time = self.time

            if self.start:
                play_sound("sfx\countdown.wav")
                self.start = False

            # 更換背景，2分鐘換一次
            if ((self.time - self.new_time) // 100 % (10 * 120) == 1199) and self.change:
                self.ground.change_ground()
                self.last_change = time.time()
                self.change = False
            # 防止重複更換
            if not self.change and (time.time() - self.last_change) > 2:
                self.change = True

            for f in fires.sprites():
                f.speed_fire = SPEED + self.speedup
            for b in buildings.sprites():
                b.speed_build = SPEED + self.speedup

            # 準備畫面
            if self.show_ready:
                self.stop_time = pygame.time.get_ticks()
                self.pause = True
                ready_time = self.draw_ready_time()
                if ready_time >= 4:
                    self.show_ready = False
                    self.pause = False
                    self.stop_time_count = 4 * 1000

            if not self.player.protected:
                # 判斷石頭與主角相撞
                hits = pygame.sprite.spritecollide(self.player, rocks, True, pygame.sprite.collide_circle)
                for hit in hits:
                    new_rock()
                    play_sound("sfx/smb_bump.wav")
                    self.player.health -= 34
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    if self.player.health <= 0:
                        self.player.health = 0
                        death_expl = Explosion(self.player.rect.center, 'player')
                        all_sprites.add(death_expl)

                # 判斷火與主角相撞
                hits = pygame.sprite.spritecollide(self.player, fires, True, pygame.sprite.collide_circle)
                for hit in hits:
                    new_fire()
                    play_sound("sfx/smb_bump.wav")
                    self.player.health -= 17
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    if self.player.health <= 0:
                        self.player.health = 0
                        death_expl = Explosion(self.player.rect.center, 'player')
                        all_sprites.add(death_expl)

                # 判斷建築物與主角相撞
                hits = pygame.sprite.spritecollide(self.player, buildings, True)
                for hit in hits:
                    new_building()
                    play_sound("sfx/smb_bump.wav")
                    self.player.health -= 17
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    if self.player.health <= 0:
                        self.player.health = 0
                        death_expl = Explosion(self.player.rect.center, 'player')
                        all_sprites.add(death_expl)

            # 判斷石頭與子彈碰撞
            hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
            for hit in hits:
                self.score += 1
                play_sound("sfx/smb_breakblock.wav")
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                if random.random() > self.update_rate:
                    pow = Power(hit.rect.center)
                    all_sprites.add(pow)
                    powers.add(pow)

                new_rock()

                self.count += 1
                self.power_count += 1

                if self.count % 200 == 0:
                    if self.score <= 200:
                        for i in range(5):
                            new_fire()
                    else:
                        self.ground.ground_speed += 2
                        self.speedup += 2
                        self.count = 0
                        for i in range(1):
                            new_rock()
                            new_fire()

                if self.power_count % 200 == 0:
                    if self.update_rate >= 0.98:
                        self.update_rate = 0.98
                    else:
                        self.update_rate += 0.02
                    self.power_count = 0

            # 判斷水球與火相撞
            hits = pygame.sprite.groupcollide(waterballs, fires, True, True)
            for hit in hits:
                self.score += 1
                play_sound("sfx/smb_bowserfire.wav")
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                new_fire()

                self.count += 1
                self.power_count += 1

                if self.count % 200 == 0:
                    if self.score >= 400:
                        self.ground.ground_speed += 2
                        self.speedup += 2
                        self.count = 0
                        for i in range(1):
                            new_rock()
                            new_fire()

                if self.power_count % 200 == 0:
                    if self.update_rate >= 0.98:
                        self.update_rate = 0.98
                    else:
                        self.update_rate += 0.02
                    self.power_count = 0

            # 判斷水球被建築擋住
            hits = pygame.sprite.groupcollide(waterballs, buildings, True, False)
            for hit in hits:
                 play_sound("sfx/smb_bump.wav")

            # 判斷子彈被建築擋住
            hits = pygame.sprite.groupcollide(bullets, buildings, True, False)
            for hit in hits:
                play_sound("sfx/smb_bump.wav")

            # 判斷寶物與主角相撞
            hits = pygame.sprite.spritecollide(self.player, powers, True)
            for hit in hits:
                if hit.type == 'blood':
                    play_sound("sfx/smb_1-up.wav")
                    self.player.health += 34
                    if self.player.health > 100:
                        self.player.health = 100
                elif hit.type == 'gun':
                    play_sound("sfx/smb_powerup_appears.wav")
                    self.player.gunup()

            # 房子跟火不要撞一起
            hits = pygame.sprite.groupcollide(buildings, fires, False, True)
            for hit in hits:
                new_fire()

            # 讓動畫播完再結束遊戲
            if self.player.health <= 0 and not (death_expl.alive()):
                self.close = True
                self.show_ready = True

            # 畫面顯示
            screen.fill(BLACK)
            self.ground.draw(screen)
            all_sprites.draw(screen)

            # 防護罩
            self.player.protected = self.protect.activated
            if self.player.protected:
                self.player.draw_protect(screen)
                self.player.p_trans -= 0.1
            else:
                self.player.p_trans = 90

            # 通殺
            if self.kill_all:
                self.player.draw_kill_all(screen)
                if self.player.k_range == 100:
                    self.kill_all = False

            self.draw_health(screen, self.player.health, 50, 20)
            self.draw_weapon_time(screen, self.protect.total_time, self.protect.max_time, 50, 50)

            self.draw_text(screen, BLACK, self.draw_time(), 40, WIDTH / 2 - 10, 15)
            self.draw_text(screen, BLACK, str(self.score).zfill(6), 40, WIDTH - 150, 15)

            #滑鼠圖示顯示
            if not self.pause and not self.close:
                pygame.mouse.set_visible(False)
                self.draw_mouse(screen, x, y)

            if self.pause:
                pygame.mouse.set_visible(True)
                self.draw_pause(screen, self.rand_num)

            if self.close:
                pygame.mouse.set_visible(True)
                self.draw_close(screen, self.rand_num2)

            # if self.player.health <= 0 and (self.time - self.new_time) <= 3000:
            #     print("虐貓小廚")
            # if self.counter == 100 and (self.time - self.new_time) <= 10000:
            #     print("百步穿楊")

            pygame.display.update()

        # pygame.quit()
        