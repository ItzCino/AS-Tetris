# Tetris Game by Zhi Feng Chen
# Customizeable Tetris game which allows for custom gamemodes and pieces

# import modules
import pygame
from Tetris import mainMenu
from Common import window_size

pygame.init()

# event main loop
def main_loop():
    running_state = True
    while running_state:
        main_window = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()
        mainMenu(main_window, clock)

# checks to ensure this TetrisMain.py is the file being run before main program executes
if __name__ == '__main__':
    main_loop()
