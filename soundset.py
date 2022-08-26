'''play_sound module'''
import pygame
import os

# 播放音效（只支援 wav）
_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        temp = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(temp)
        sound.set_volume(0.2)
        _sound_library[path] = sound
    sound.play()