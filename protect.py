import pygame
from setting import FPS
from soundset import play_sound

class Protect:
    def __init__(self):
        self.max_time = 60 * FPS
        self.total_time = 12 * FPS
        self.activated = False
        self.to_zero = True

    def is_ready(self) -> bool:
        if self.total_time >= self.max_time >= self.max_time:
            # 經過60秒
            return True
        else:
            return False

    def update(self):
        self.total_time += 1
        if self.total_time >= self.max_time:
            self.total_time = self.max_time

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LSHIFT] and self.is_ready():
            self.activated = True

        # 確保只會扣一次
        if self.activated and self.to_zero:
            play_sound("sfx\smb3_raccoon_transform.wav")
            self.total_time = 0
            self.to_zero = False

        # 效果時間12秒
        if self.total_time >= self.max_time // 5:
            self.activated = False

        if not self.activated and self.is_ready():
            self.to_zero = True
