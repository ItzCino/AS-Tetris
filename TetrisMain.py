# Tetris Game by Zhi Feng Chen 
# Customizeable Tetris game which allows for custom gamemodes and pieces

#import modules
import pygame
import random
import time
import pprint

acceleration = 0.2
# dropCounter = 0

window_width = 1200
window_height = 800
window_size = (window_width, window_height)

linesCleared = 0
gameGridPosX = 425 
gameGridPosY = 50
blockSize = 35
columns = 10
rows = 20

# main_window = pygame.display.set_mode(window_size)
# clock = pygame.time.Clock()

pygame.init()
FPS = 20

# Colors for pieces
red = (192, 0, 0)
orange = (255, 165, 0)
yellow = (192, 192, 0)
green = (0, 192, 0)
blue = (0, 0, 192)
cyan = (0, 192, 192)
purple = (138,43,226)

block_colors = [purple, orange, blue, cyan, red, green, yellow, (255, 255, 255)]

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


squareColor = black

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

blockData = []
gridData = []

tetris_data = [
    # T shape 1
    [
      ['.o.',
       'ooo'],
      [
       'o.',
       'oo',
       'o.'],
      [
       'ooo',
       '.o.'],
      [
       '.o',
       'oo',
       '.o'],
     ],
    # L Shape 2:
    [['o.',
      'o.',
      'oo'],
     [
      'ooo',
      'o..'],
     [
      'oo',
      '.o',
      '.o'],
     [
      '..o',
      'ooo']],
    # L Shape flipped 3:
    [['.o',
      '.o',
      'oo'],
     [
      'o..',
      'ooo',
      ],
     [
      'oo',
      'o.',
      'o.'
      ],
     [
      'ooo',
      '..o',
      ]],
    # I Shape 4:
    [[
      'o',
      'o',
      'o',
      'o'],
     [
      'oooo']],
    # Z Shape 5:
    [[
      'oo.',
      '.oo'],
     [
      '.o',
      'oo',
      'o.']],

    # Z Flipped 6:
    [[
      '.oo',
      'oo.'],
     [
      'o.',
      'oo',
      '.o']],
    # Box Shape 7:
    [[
      'oo',
      'oo']],
    [[
        '..o..',
        '..o..',
        '..o..',
        '..o..',
        'oo.oo',
        'o...o'

    ]]
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
        self.x = (gameGridPosX - blockSize + columns // 2 * blockSize)
        self.y = gameGridPosY
        self.bottomCord = gameGridPosY + (rows * blockSize)
        self.rightCord = gameGridPosX + (columns * blockSize)
        self.rawRotationValue = 0
        self.rotation = 0
        self.shape = random.randint(0, len(blockData) - 1)
        self.color = block_colors[self.shape]
        self.dropCounter = 0

        # print(self.x, self.y)


    def placePiece(self, gridData):
        gridX = (self.x - gameGridPosX) // blockSize 
        gridY = (self.y - gameGridPosY) // blockSize
        while True:
            if self.pieceInDirection('down', 0, None, gridY) is True:
                break
            else:
                gridY += 1
        print('out\nout')
        for coordinates in blockData[self.shape][self.rotation]:
            x = coordinates[0] 
            y = coordinates[1]
            # print(x, y)
            gridData[gridX + x][gridY + y] = self.color


    def drawPiece(self, surface):
        # print(self.shape)
        # takes the rotation index of the piece that was selected.
        # print(self.shape)   
        self.rotation = self.rawRotationValue % len(blockData[self.shape])
        # print(self.rawRotationValue, self.rotation)
        
        for coordinates in blockData[self.shape][self.rotation]:
            x = coordinates[0] 
            y = coordinates[1]
            # Draws each square of each shape in relation to self.x and self.y position
            pygame.draw.rect(surface, block_colors[self.shape], 
                                    (x * blockSize + self.x, 
                                    y * blockSize + self.y, 
                                    blockSize, blockSize))


    def bottomGrid(self):
        bottomGrid = False
        gridX = round((self.x - gameGridPosX) / blockSize)    
        gridY = round((self.y - gameGridPosY) / blockSize)
        for coordinates in blockData[self.shape] \
        [(self.rawRotationValue) % len(blockData[self.shape])]:
            x = coordinates[0] + gridX
            y = coordinates[1] + gridY
            # print(x, y)
            if y < 0 or y > (rows - 1):
                print('pieceInRotation = true')
                bottomGrid = True
                return bottomGrid
            if gridData[x][y] != squareColor:
                bottomGrid = True

        return bottomGrid


# checks that the piece isn't out of grid before rotating
# checks that the piece collide with other pieces before rotating
    def rotationBoundaryCheck(self):
        pieceInRotation = False
        gridX = round((self.x - gameGridPosX) / blockSize)    
        gridY = round((self.y - gameGridPosY) / blockSize)
        for coordinates in blockData[self.shape] \
        [(self.rawRotationValue + 1) % len(blockData[self.shape])]:
            x = coordinates[0] + gridX
            y = coordinates[1] + gridY
            # print(x, y)
            if 0 > x or x > (columns - 1) or     \
                  y < 0 or y > (rows - 1):
                print('pieceInRotation = true')
                pieceInRotation = True
                return pieceInRotation
            if gridData[x][y] != squareColor:
                pieceInRotation = True

        return pieceInRotation


    # renamed from boundaryCheck to pieceInDirection
    def pieceInDirection(self, direction, rotation=0, 
                            currentPosX=None, currentPosY=None):      
        pieceInDirection = False
        if currentPosX is None:
            gridX = round((self.x - gameGridPosX) / blockSize)
        else:
            gridX = currentPosX

        if currentPosY is None:
            gridY = round((self.y - gameGridPosY) / blockSize)
        else:
            gridY = currentPosY

        try:
            for coordinates in blockData[self.shape]                 \
                [(self.rawRotationValue + rotation) %                \
                len(blockData[self.shape])]:    
                x = coordinates[0] + gridX
                y = coordinates[1] + gridY
                
                if direction == 'up':
                    if gridData[x][y - 1] != squareColor:
                        pieceInDirection = True
                    if 0 > x or x > (columns - 1) or                 \
                  (y - 1) < 0 or (y - 1) > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
                if direction == 'down':
                    if gridData[x][y + 1] != squareColor:
                        pieceInDirection = True
                    if 0 > x or x > (columns - 1) or                  \
                  (y + 1) < 0 or (y + 1) > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
                if direction == 'left':
                    if gridData[x - 1][y] != squareColor:
                        pieceInDirection = True
                    if 0 > (x - 1) or (x - 1) > (columns - 1) or       \
                  y < 0 or y > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
                if direction == 'right':
                    if gridData[x + 1][y] != squareColor:
                        pieceInDirection = True
                    if 0 > (x + 1) or (x + 1) > (columns - 1) or        \
                  y < 0 or y > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
        except IndexError:
            pieceInDirection = True
        # print(pieceInDirection)
        return pieceInDirection


    def assistRotate(self):
        rotated = False
        # print('before:', self.rawRotationValue)
        if rotated == False and self.pieceInDirection('down', 1) == False:
            self.rawRotationValue += 1
            self.y += blockSize
            rotated = True

        if rotated == False and self.pieceInDirection('left', 1) == False:
            self.rawRotationValue += 1
            self.x -= blockSize
            rotated = True

        if rotated == False and self.pieceInDirection('right', 1) == False:
            self.rawRotationValue += 1
            self.x += blockSize
            rotated = True
        
        if rotated == False and self.pieceInDirection('up', 1) == False:
            self.rawRotationValue += 1
            self.y -= blockSize
            rotated = True

        # print('after:', self.rawRotationValue)  


    def rotate(self):
        if self.rotationBoundaryCheck() == False:
            self.rawRotationValue += 1
            self.rotation = self.rawRotationValue % len(blockData[self.shape])
        else:
            self.assistRotate()


    def moveUp(self):
        if (self.y - blockSize) >= gameGridPosY:
            if self.pieceInDirection('up') == False:
                self.y -= blockSize


    def moveDown(self):
        pieceInDirection = self.pieceInDirection('down')

        if (self.y + (len(tetris_data[self.shape]\
        [self.rotation]) * blockSize)) < self.bottomCord:
            if pieceInDirection == False:
                self.dropCounter = 0
                self.y += blockSize
                print('NOT placed')
        if pieceInDirection == True:
            # self.placePiece(gridData)
            print('placed')
        
        return pieceInDirection
# bottomGrid
    def moveLeft(self):
        if (self.x - blockSize) >= gameGridPosX:
            if self.pieceInDirection('left') == False:
                self.x -= blockSize


    def moveRight(self):
        if (self.x + (len(tetris_data[self.shape][self.rotation][0]) * blockSize)) < self.rightCord:
            if self.pieceInDirection('right') == False:
                self.x += blockSize


    def checkCords(self):
        # print(self.x, self.y)
        # print(self.rawRotationValue)
        pass


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
    finishedGrid = []
    finishedGrid = [[squareColor for row in range(rows)] for column in range(columns)]

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
    linesCleared = 0
    helpButton = main_menu_buttons("Back", 85,  white, orange, darkerOrange, 20, 20, lambda: mainMenu(main_window, clock), 225, 125)
    # gridData = createGrid(rows, columns)
    while True:
        if piece == None:
            piece = tetrisPiece()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                # this key will be changed to
                # up arrow key once prog is finished
                if keys[pygame.K_r]:
                    piece.rotate()
                    if piece == None:
                        piece = tetrisPiece()
                if keys[pygame.K_SPACE]:
                    piece.placePiece(gridData)
                    piece = None
                    if piece == None:
                        piece = tetrisPiece()
                if keys[pygame.K_ESCAPE]:
                    piece = None
                    if piece == None:
                        piece = tetrisPiece()
        if piece == None:
            piece = tetrisPiece()
        # print(piece.x, piece.y)
        # clock.tick(20)
        # time.sleep(0.2)
        # piece.moveDown()
        
        main_window.fill(lightGrey)
        helpButton.drawButton(main_window, 8, False, True, darkOrange)
        piece.checkCords()
        drawGrid(main_window, gameGridPosX, gameGridPosY, rows, columns, blockSize, gridData, piece)
        # piece.drawPiece(main_window)
        gridX = round((piece.x - gameGridPosX) / blockSize)    
        gridY = round((piece.y - gameGridPosY) / blockSize)
        
        # print('grid: ',gridX, gridY)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            piece.moveUp()
            # print("UP")
        if keys[pygame.K_DOWN]:
            # piece.moveDown()
            if piece.moveDown() == True:
                piece.dropCounter = 0
                # piece = tetrisPiece()
            # print("DOWN")
        if keys[pygame.K_LEFT]:
            piece.moveLeft()
            # print("LEFT")
        if keys[pygame.K_RIGHT]:
            piece.moveRight()
 
        if piece.dropCounter < FPS :
            piece.dropCounter += (1 + linesCleared *acceleration)
        else:
            if piece.moveDown() == True:
                piece.placePiece(gridData)
                piece = tetrisPiece()
            piece.dropCounter = 0


        # linesCleared += 1

        # print('rate: ', (1 + linesCleared *0.5))
        # print('lines cleared: ', linesCleared)

        # print(linesCleared)
        # piece.drawPiece(main_window)

        # exitButton.drawButton(main_window, 8, False, True, darkRed)
        
        clock.tick(FPS)
        pygame.display.update()


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
    gridData = createGrid(rows, columns)

    main_loop()




