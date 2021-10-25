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
    main_menu_font = pygame.font.SysFont("Arial", 110)

    return main_menu, running, clock, main_menu_font


#draws texts for the future buttons onto screen
# def draw_text(text, font, buttonColor, fontColor, surface, x, y):
#     text_object = font.render(text, 10, fontColor)
#     text_rect = text_object.get_rect()
#     text_rect.topleft = (x, y)
#     pygame.draw.rect(surface, buttonColor,text_rect)
#     surface.blit(text_object, text_rect)

class main_menu_buttons:
    def __init__(self, text, x, y, width, height, fontColor):
        self.text = text
        self.x = x
        self.y = y
        self.pos= (x, y)
        self.width = width
        self.height = height
        self.fontColor = fontColor
        self.text_rect = None


    def hoveringOverButton(self):
        # Gets mouse position.
        mouse_position = pygame.mouse.get_pos()
        # checks for when mouse is inside the button in the x and y directions.
        if mouse_position[0] > self.text_rect[0] and mouse_position[0] < window_width - self.text_rect[0]:
            if mouse_position[1] > self.text_rect[1] and mouse_position[1] < self.y + self.text_rect[1]:
                # If inside the button do this:
                print(self.text)
        else:
            # Otherwise do this:
            print('out')
        # print(mouse_position)



    def drawButton(self, window, buttonColor, padding, autoCenter=False, 
                                        outline=False, outlineColor=None):
        main_menu_font = pygame.font.SysFont("Arial", 100)
        text_object = main_menu_font.render(self.text, 10, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos

        if autoCenter:
            buttonWidth = text_rect[2]
            center = (window_width / 2) - (buttonWidth / 2)
            text_rect[0] = center

        if outline:
            pygame.draw.rect(window, outlineColor, (text_rect[0] - padding, 
                                                    text_rect[1] - padding, 
                                                    text_rect[2] + 2*padding, 
                                                    text_rect[3] + 2*padding))

        self.text_rect = text_rect
        pygame.draw.rect(window, buttonColor, text_rect)
        window.blit(text_object, text_rect)
    



# event main loop
def main_loop():
    main_window, running_state, clock, main_menu_font = init()
    clockTick = 1
    while running_state:
        main_window.fill((200,200,200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        # draw_text('Play', main_menu_font, (96, 169, 23),(255, 255, 255), main_window, 500, 200)
        button = main_menu_buttons("Play", 0, 100, 200, 200, (255,255,255))
        button.drawButton(main_window, (96, 169, 23), 8, True, True, (45, 118, 0))
        button.hoveringOverButton()

        button = main_menu_buttons("Help", 0, 300, 200, 200, (255,255,255))
        button.drawButton(main_window, (250, 104, 0), 8, True, True, (199, 53, 0))
        button.hoveringOverButton()

        button = main_menu_buttons("Exit", 0, 500, 200, 200, (255,255,255))
        button.drawButton(main_window, (229, 20, 0), 8, True, True, (178, 0, 0))
        button.hoveringOverButton()
        clockTick = myclock(clockTick)
        clock.tick(FPS)
        pygame.display.update()

        # myButton = button((255, 255, 255), 500, 500, 300, 100, "HELLO")
        


if __name__ == '__main__':
    main_loop()




