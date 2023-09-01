from pygame.mouse import get_pressed as get_mouse_pressed, get_pos as get_mouse_pos
from Common import window_width
from pygame.font import SysFont as generate_font
from pygame.draw import rect as draw_rect


# Creates buttons class
class main_menu_buttons:
    def __init__(self, text, fontSize, fontColor, buttonColor, hoveringColor, x, y, func, width=None, height=None):
        self.text = text
        self.fontSize = fontSize
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.fontColor = fontColor
        self.text_rect = None
        self.buttonColor = buttonColor
        self.hoveringColor = hoveringColor
        self.currentButtonColor = buttonColor
        self.func = func

    # check for mouse click and enables 'hovering' colors
    def hoveringOverButton(self):
        # Gets mouse position.
        mouse_position = get_mouse_pos()
        # checks for when mouse is inside the button in the x and y directions.
        if mouse_position[0] > self.text_rect[0] and mouse_position[0] < self.text_rect[0] + self.text_rect[2]:
            if mouse_position[1] > self.text_rect[1] and mouse_position[1] < self.y + self.text_rect[3]:
                # If inside the button do this: Change color of button
                self.currentButtonColor = self.hoveringColor
                # Clicking Code Here
                keys = get_mouse_pressed()
                if keys[0]:
                    print("Hovering button")
                    self.func()

            else:
                # Otherwise do this: Revert Color of button to original color
                self.currentButtonColor = self.buttonColor

        else:
            # Otherwise do this: Revert Color of button to original color
            self.currentButtonColor = self.buttonColor

    # Draws button to screen
    def drawButton(self, window, padding, autoCenter=False, outline=False, outlineColor=None):
        main_menu_font = generate_font("Arial", self.fontSize)
        text_object = main_menu_font.render(self.text, 5, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos

        # Draws background area for button
        if self.width is not None:
            text_rect[2] = self.width

        if self.height is not None:
            text_rect[3] = self.height

        if autoCenter:
            buttonWidth = text_rect[2]
            center = (window_width / 2) - (buttonWidth / 2)
            text_rect[0] = center

        if outline:
            draw_rect(window, outlineColor, (text_rect[0] - padding,
                                                    text_rect[1] - padding,
                                                    text_rect[2] + 2 * padding,
                                                    text_rect[3] + 2 * padding))

        self.text_rect = text_rect
        self.hoveringOverButton()

        draw_rect(window, self.currentButtonColor, text_rect)

        # Centering of text for button
        # Calculates the Topleft position for centering button

        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos

        # Gets width + Height of the text object
        textDimensions = main_menu_font.size(self.text)

        # Centering of text for button
        centerOfButtonX = text_rect[0] + (self.width // 2) - (textDimensions[0] // 2)
        centerOfButtonY = text_rect[1] + (self.height // 2) - (textDimensions[1] // 2)
        newPos = (centerOfButtonX, centerOfButtonY)

        text_rect.topleft = newPos

        # Centers TEXT to middle of the window; Horizontally
        if autoCenter:
            buttonWidth = text_rect[2]
            center = (window_width / 2) - (buttonWidth / 2)
            text_rect[0] = center

        window.blit(text_object, text_rect)