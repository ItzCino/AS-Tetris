# Tetris Game by Zhi Feng Chen 
# Customizeable Tetris game which allows for custom gamemodes and pieces

#import modules
import pygame
import random

window_width = 1200
window_height = 800
window_size = (window_width, window_height)
FPS = 60


# Initalisation 
def init():
    main_menu = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    running = True
    pygame.init()
    font = pygame.font.SysFont(None, 125)

    return main_menu, running, clock, font


#draws texts for the future buttons onto screen
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 10, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)


# event main loop
def main_loop():
    main_window, running_state, clock, font = init()
    while running_state:
        main_window.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        draw_text('Play', font, (255, 255, 255), main_window, 500, 200)
        clock.tick(FPS)
        pygame.display.update()

        # myButton = button((255, 255, 255), 500, 500, 300, 100, "HELLO")
        


if __name__ == '__main__':
    main_loop()


