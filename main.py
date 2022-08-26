'''貓貓救援大作戰'''
import pygame
from start_menu import StartMenu

if __name__ == '__main__':
    pygame.init()
    main = StartMenu()
    main.menu_run()