# Tetris Game by Zhi Feng Chen 
# Customizeable Tetris game which allows for custom gamemodes and pieces

#import modules
import pygame
import random

window_width = 1200
window_height = 800
window_size = (window_width, window_height)
FPS = 60

# timer
def myclock(clock):
    if clock == 60:
        # print("1 sec had passed")
        clock = 1
        return clock
    else:
        clock += 1
        # print(clock)
        return clock


# Initalisation 
def init():
    main_menu = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    running = True
    pygame.init()
    main_menu_font = pygame.font.SysFont("Arial", 125)

    return main_menu, running, clock, main_menu_font


#draws texts for the future buttons onto screen
def draw_text(text, font, buttonColor, fontColor, surface, x, y):
    text_object = font.render(text, 10, fontColor)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    pygame.draw.rect(surface, buttonColor,text_rect)
    surface.blit(text_object, text_rect)


# event main loop
def main_loop():
    main_window, running_state, clock, main_menu_font = init()
    clockTick = 1
    while running_state:
        main_window.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        draw_text('Play', main_menu_font, (96, 169, 23),(255, 255, 255), main_window, 500, 200)
        clockTick = myclock(clockTick)
        clock.tick(FPS)
        pygame.display.update()

        # myButton = button((255, 255, 255), 500, 500, 300, 100, "HELLO")
        


if __name__ == '__main__':
    main_loop()


