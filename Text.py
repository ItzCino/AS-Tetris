from Common import window_width
# from pygame.font import SysFont as generate_font
import pygame.sysfont as font 



# Text Class
class createText:
    def __init__(self, text, fontSize, fontColor, x, y):
        self.text = text
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.x = x
        self.y = y

    # Draws text to screen + centers it if autoCenter is True
    def drawText(self, window, autoCenter=False, startingXPos=None, endingXPos=None):
        if startingXPos is None:
            startingXPos = window_width / 2
        if endingXPos is None:
            endingXPos = window_width / 2
        centerX = (startingXPos + endingXPos) / 2

        main_menu_font = font.SysFont("Arial", self.fontSize)
        text_object = main_menu_font.render(self.text, 5, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = (self.x, self.y)

        textDimensions = main_menu_font.size(self.text)
        # centers the text on the x axis of the window if True
        if autoCenter:
            text_rect[0] = centerX - (textDimensions[0] / 2)
        window.blit(text_object, text_rect)

def blank():
    return