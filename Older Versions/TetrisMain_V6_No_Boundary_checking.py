# Tetris Game by Zhi Feng Chen 
# Customizeable Tetris game which allows for custom gamemodes and pieces

#import modules
import pygame
import random
import time
import pprint

window_width = 1200
window_height = 800
window_size = (window_width, window_height)

gameGridPosX = 425
gameGridPosY = 50
blockSize = 35
columns = 10
rows = 20

# main_window = pygame.display.set_mode(window_size)
# clock = pygame.time.Clock()
pygame.init()
FPS = 60

# Colors for pieces
red = (192, 0, 0)
orange = (255, 165, 0)
yellow = (192, 192, 0)
green = (0, 192, 0)
blue = (0, 0, 192)
cyan = (0, 192, 192)
purple = (138,43,226)

block_colors = [purple, orange, blue, cyan, red, green, yellow]

# Colors

black = (0, 0, 0)
white = (255,255,255)

green = (96, 169, 23)
darkerGreen = (50, 75, 10)
darkGreen = (45, 118, 0)

orange = (250, 104, 0)
darkerOrange = (199, 53, 0)
darkOrange = (125, 50, 0)

red = (229, 20, 0)
darkerRed = (178, 0, 0)
darkRed = (115, 10, 0)

lightGrey = (200,200,200)
grey = (100, 100, 100)
darkGrey = (75, 75, 75)




RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

thing = []

tetris_data = [
    # T shape 1
    [
      ['..o.',
       '.ooo'],
      [
       '.o.',
       '.oo',
       '.o.'],
      [
       '.ooo',
       '..o.'],
      [
       '..o',
       '.oo',
       '..o'],
     ],
    # L Shape 2:
    [['.o.',
      '.o.',
      '.oo'],
     [
      '.ooo',
      '.o..'],
     [
      '.oo',
      '..o',
      '..o'],
     [
      '...o',
      '.ooo']],
    # L Shape flipped 3:
    [['..o',
      '..o',
      '.oo'],
     [
      '.o...',
      '.oooo',
      ],
     [
      '.oo',
      '.o.',
      '.o.',
      '.o.'],
     [
      '.ooo',
      '...o',
      ]],
    # I Shape 4:
    [[
      '.o',
      '.o',
      '.o',
      '.o'],
     [
      '.oooo']],
    # Z Shape 5:
    [[
      '.oo.',
      '..oo'],
     [
      '..o',
      '.oo',
      '.o.']],

    # Z Flipped 6:
    [[
      '..oo',
      '.oo.'],
     [
      '.o.',
      '.oo',
      '..o']],
    # Box Shape 7:
    [[
      '.oo',
      '.oo']]
]


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

# Text Class
class createText:
    def __init__(self, text, fontSize, fontColor, x, y):
        self.text = text
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.x = x
        self.y = y

    # Draws text to screen
    def drawText(self, window, autoCenter=False):
        main_menu_font = pygame.font.SysFont("Arial", self.fontSize)
        text_object = main_menu_font.render(self.text, 5, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = (self.x, self.y)
    
        textDimensions = main_menu_font.size(self.text)
        # centers the text on the x axis of the window if True
        if autoCenter:
            text_rect[0] = (window_width / 2) - (textDimensions[0] / 2)
        # print(textDimensions)
        window.blit(text_object, text_rect)




class main_menu_buttons:
    def __init__(self, text, fontSize, fontColor, buttonColor, hoveringColor, 
                        x, y, func, width=None, height=None):
        self.text = text
        self.fontSize = fontSize
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
        self.func = func


    def hoveringOverButton(self):
        # Gets mouse position.
        mouse_position = pygame.mouse.get_pos()
        # checks for when mouse is inside the button in the x and y directions.
        if mouse_position[0] > self.text_rect[0] and mouse_position[0] < self.text_rect[0] + self.text_rect[2]:
            if mouse_position[1] > self.text_rect[1] and mouse_position[1] < self.y + self.text_rect[3]:
                # If inside the button do this: Change color of button
                self.currentButtonColor = self.hoveringColor
                    #Clicking Code Here
                keys = pygame.mouse.get_pressed()
                if keys[0]:
                    print("in")
                    self.func()


            else:
                # Otherwise do this: Revert Color of button to original color
                self.currentButtonColor = self.buttonColor

        else:
            # Otherwise do this: Revert Color of button to original color
            self.currentButtonColor = self.buttonColor
        # print(mouse_position)
        # print(self.currentButtonColor)



    def drawButton(self, window, padding, autoCenter=False, 
                                outline=False, outlineColor=None):
        main_menu_font = pygame.font.SysFont("Arial", self.fontSize)
        text_object = main_menu_font.render(self.text, 5, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos

        # Draws background area for button

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
        # print('before: ',text_rect)
        
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos


        # Gets width + Height of the text object
        textDimensions = main_menu_font.size(self.text)

        # print(main_menu_font.size(self.text))
        # Centering of text for button
        centerOfButtonX = text_rect[0] + (self.width//2) - (textDimensions[0] // 2)
        centerOfButtonY = text_rect[1] + (self.height//2) - (textDimensions[1] // 2)
        newPos = (centerOfButtonX, centerOfButtonY)
        # print('after: ', newPos)
        # print((text_rect[2]//2), (textDimensions[0] // 2))
        # print(text_rect[2], text_rect[3])

        text_rect.topleft = newPos
        
        # Centers TEXT to middle of the window; Horizontally
        if autoCenter:
            buttonWidth = text_rect[2]
            center = (window_width / 2) - (buttonWidth / 2)
            text_rect[0] = center



        # pygame.draw.rect(main_window, lightGrey, (newPos[0], newPos[1], 5,5))
        # pygame.draw.rect(main_window, lightGrey, text_rect, 5, 5)


        window.blit(text_object, text_rect)

class tetrisPiece:
    def __init__(self):
        self.x = gameGridPosX + 5 * blockSize
        self.y = gameGridPosY
        self.bottomCord = gameGridPosY + (rows * blockSize)
        self.rightCord = gameGridPosX + (columns * blockSize)
        self.rotation = 0
        self.shape = random.randint(0, len(blockData) - 1)


    def drawPiece(self, surface):
        print(self.shape)
        for coordinates in blockData[self.shape][self.rotation % len(blockData[self.shape])]:
            x = coordinates[0] - 1
            y = coordinates[1]
            
            pygame.draw.rect(surface, block_colors[self.shape], (x * blockSize + self.x, y * blockSize + self.y, blockSize, blockSize))
            # print(coordinates)    

    # def drawPiece(self, surface):
    #     pygame.draw.rect(surface, red, 
    #                     (self.x, self.y, 
    #                     blockSize, blockSize))

    def rotate(self):
        self.rotation += 1

    def moveUp(self):
        if (self.y - blockSize) >= gameGridPosY:
            self.y -= blockSize

    def moveDown(self):
        if (self.y + blockSize) < self.bottomCord:
            self.y += blockSize

    def moveLeft(self):
        if (self.x - blockSize) >= gameGridPosX:
            self.x -= blockSize

    def moveRight(self):
        if (self.x + blockSize) < self.rightCord:
            self.x += blockSize

    def checkCords(self):
        print(self.x, self.y)


def convertTetrisData(blockData):
    positions = []
    for shape in blockData:
        temp_shape = []
        for orientation in shape:
            temp_orientation = []
            line_count = 0
            for line in orientation:
                position_count = 0
                for block in line:
                    if block == 'o':
                        temp_orientation.append((position_count, line_count))
                    position_count += 1
                line_count += 1
            temp_shape.append(temp_orientation)
        positions.append(temp_shape)
    print(positions)
    return positions
    

def createGrid(rows, columns):
    # change this to grey later
    black = (0, 0, 0)
    finishedGrid = []
    finishedGrid = [[(black) for row in range(rows)] for column in range(columns)]

    return finishedGrid


# Draws a 10 x 20 grid 
def drawGrid(surface, x, y, rows, columns, blockSize, gridData, piece):

    width = columns * blockSize
    height = rows * blockSize
    startX = x
    startY = y

    # Fills in the grid with a darker shade of grey
    # pygame.draw.rect(surface, (150, 150, 150), (x,y,width,height))
    
    


    # displays colors / pieces on the grid
    for column in range(0, len(gridData)):
        for row in range(0, len(gridData[0])):
            pygame.draw.rect(surface, (gridData[column])[row], 
                            (startX + (blockSize*column), 
                            startY + (blockSize*row), 
                            blockSize, blockSize))

    piece.drawPiece(surface)
    

    # Draws Vertical lines
    for column in range(columns):
        pygame.draw.line(surface, grey, (x, y) ,(x, y + height), 2)
        x += blockSize

    # Draws Horizontal Lines
    x = startX
    for row in range(rows):
        pygame.draw.line(surface, grey, (x, y) ,(x + width, y), 2)
        y += blockSize
    y = startY
    
    # Creates Border
    pygame.draw.rect(surface, darkGrey, (x,y,width,height), 5)
    # print(x,y)
    

    # exit()

def gameLoop(main_window, clock):
    # exitButton = main_menu_buttons("Exit", 100, white, red, darkerRed, 400, 550, exit, 210, 125) 
    piece = None
    helpButton = main_menu_buttons("Back", 85,  white, orange, darkerOrange, 20, 20, lambda: mainMenu(main_window, clock), 225, 125)
    gridData = createGrid(rows, columns)
    i=0
    while True:
        if piece is None:
            piece = tetrisPiece()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        clock.tick(20)
        
        main_window.fill(lightGrey)
        helpButton.drawButton(main_window, 8, False, True, darkOrange)
        piece.checkCords()
        drawGrid(main_window, gameGridPosX, gameGridPosY, rows, columns, blockSize, gridData, piece)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            piece.moveUp()
            # print("UP")
        if keys[pygame.K_DOWN]:
            piece.moveDown()
            # print("DOWN")
        if keys[pygame.K_LEFT]:
            piece.moveLeft()
            # print("LEFT")
        if keys[pygame.K_RIGHT]:
            piece.moveRight()
            # print("RIGHT")
        if keys[pygame.K_r]:
            piece.rotate()
        if keys[pygame.K_ESCAPE]:
            piece = None
        # if keys[pygame.K_SPACE]:
        #     piece.placePiece()

        # if i < 30:
        #     i += 1
        # else:
        #     piece.moveDown()

        #     i = 0
        

        
        # piece.drawPiece(main_window)

        # exitButton.drawButton(main_window, 8, False, True, darkRed)
        
        clock.tick(FPS)
        pygame.display.update()
    print(namer)


def helpWindow(main_window, clock):
    helpButton = main_menu_buttons("Back", 85,  white, orange, darkerOrange, 20, 20, lambda: mainMenu(main_window, clock), 225, 125)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        main_window.fill(lightGrey)
        helpButton.drawButton(main_window, 8, False, True, darkOrange)

        clock.tick(FPS)
        pygame.display.update()


def exitGame(main_window, clock):
    exitButton = main_menu_buttons("Exit", 100,  white, red, darkerRed, 390, 550, exit, 300, 125)
    while True:
        main_window.fill(lightGrey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        exitButton.drawButton(main_window, 8, True, True, darkRed)
        clock.tick(FPS)
        pygame.display.update() 
    

def mainMenu(main_window, clock):
    pygame.display.set_caption("Main Menu")
    tetris = createText('TETRIS', 100, darkGrey, 390, 35)
    playButton = main_menu_buttons("Play", 70, white, green, darkerGreen, 390, 200, lambda: gameLoop(main_window, clock), 325, 125)
    helpButton = main_menu_buttons("Help", 70,  white, orange, darkerOrange, 390, 375, lambda: helpWindow(main_window, clock), 325, 125)
    exitButton = main_menu_buttons("Exit", 70,  white, red, darkerRed, 390, 550, lambda: exitGame(main_window, clock), 325, 125)
    while True:
        main_window.fill(lightGrey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        tetris.drawText(main_window, True)
        playButton.drawButton(main_window, 8, True, True, darkGreen)
        helpButton.drawButton(main_window, 8, True, True, darkOrange)
        exitButton.drawButton(main_window, 8, True, True, darkRed)
        clock.tick(FPS)
        pygame.display.update()
        

# event main loop
def main_loop():
    running_state = True
    clockTick = 1
    while running_state:
        # main_window.fill(lightGrey)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         exit()
        main_window = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()
        mainMenu(main_window, clock)
        # clockTick = myclock(clockTick)
        # clock.tick(FPS)
        # pygame.display.update()

        # myButton = button((255, 255, 255), 500, 500, 300, 100, "HELLO")
        


if __name__ == '__main__':
    blockData = convertTetrisData(tetris_data)
    main_loop()




