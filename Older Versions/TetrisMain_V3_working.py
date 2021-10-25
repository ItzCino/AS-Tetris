# Tetris Game by Zhi Feng Chen 
# Customizeable Tetris game which allows for custom gamemodes and pieces

#import modules
import pygame
import random
import time

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

    return main_menu, running, clock


class main_menu_buttons:
    def __init__(self, text, fontColor, buttonColor, hoveringColor, 
                        x, y, width=None, height=None):
        self.text = text
        self.x = x
        self.y = y
        self.pos= (x, y)
        self.width = width
        self.height = height
        self.fontColor = fontColor
        self.text_rect = None
        self.buttonColor = buttonColor
        self.hoveringColor = hoveringColor
        self.currentButtonColor = buttonColor


    def hoveringOverButton(self):
        # Gets mouse position.
        mouse_position = pygame.mouse.get_pos()
        # checks for when mouse is inside the button in the x and y directions.
        if mouse_position[0] > self.text_rect[0] and mouse_position[0] < window_width - self.text_rect[0]:
            if mouse_position[1] > self.text_rect[1] and mouse_position[1] < self.y + self.text_rect[3]:
                # If inside the button do this: Change color of button
                self.currentButtonColor = self.hoveringColor
        else:
            # Otherwise do this: Revert Color of button to original color
            self.currentButtonColor = self.buttonColor
        # print(mouse_position)
        print(self.currentButtonColor)



    def drawButton(self, window, padding, autoCenter=False, 
                                outline=False, outlineColor=None):
        main_menu_font = pygame.font.SysFont("Arial", 100)
        text_object = main_menu_font.render(self.text, 10, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos


        if self.width != None:
            text_rect[2] = self.width

        if self.height != None:
            text_rect[3] = self.height

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
        self.hoveringOverButton()
        

        pygame.draw.rect(window, self.currentButtonColor, text_rect)

        # Centering of text for button
        # Calculates the Topleft position for centering button
        
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos

        if autoCenter:
            buttonWidth = text_rect[2]
            center = (window_width / 2) - (buttonWidth / 2)
            text_rect[0] = center
        window.blit(text_object, text_rect)
    



# event main loop
def main_loop():
    main_window, running_state, clock = init()
    clockTick = 1
    while running_state:
        main_window.fill((200,200,200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        playButton = main_menu_buttons("Play",(255,255,255), (96, 169, 23), (50, 75, 10), 0, 100, 210, 125)
        playButton.drawButton(main_window, 8, True, True, (45, 118, 0))
        # playButton.hoveringOverButton()

        helpButton = main_menu_buttons("Help", (255,255,255), (250, 104, 0), (125, 50, 0), 0, 300, 210, 125)
        helpButton.drawButton(main_window, 8, True, True, (199, 53, 0))
        # helpButton.hoveringOverButton()

        exitButton = main_menu_buttons("Exit", (255,255,255), (229, 20, 0), (115, 10, 0), 0, 500, 210, 125)
        exitButton.drawButton(main_window, 8, True, True, (178, 0, 0))
        # exitButton.hoveringOverButton()
        clockTick = myclock(clockTick)
        clock.tick(FPS)
        pygame.display.update()

        # myButton = button((255, 255, 255), 500, 500, 300, 100, "HELLO")
        


if __name__ == '__main__':
    main_loop()




