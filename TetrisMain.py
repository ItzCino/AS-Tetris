# Tetris Game by Zhi Feng Chen
# Customizeable Tetris game which allows for custom gamemodes and pieces

# import modules
import pygame
import random

acceleration = 0.2

window_width = 1200
window_height = 900
window_size = (window_width, window_height)

linesCleared = 0
gameGridPosX = 425
gameGridPosY = 50
blockSize = 35
columns = 10
rows = 23

pygame.init()
FPS = 15

# Colors for pieces
red = (192, 0, 0)
orange = (255, 165, 0)
yellow = (192, 192, 0)
green = (0, 192, 0)
blue = (0, 0, 192)
cyan = (0, 192, 192)
purple = (138, 43, 226)

block_colors = [purple, orange, blue, cyan, red, green, yellow, (255, 255, 255)]

# Colors

black = (0, 0, 0)
white = (255, 255, 255)

green = (96, 169, 23)
darkerGreen = (50, 75, 10)
darkGreen = (45, 118, 0)

orange = (250, 104, 0)
darkerOrange = (199, 53, 0)
darkOrange = (125, 50, 0)

red = (229, 20, 0)
darkerRed = (178, 0, 0)
darkRed = (115, 10, 0)

lightGrey = (200, 200, 200)
grey = (100, 100, 100)
darkGrey = (75, 75, 75)


squareColor = black

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

blockData = []

# Custom tetris pieces
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
        'ooo',
        'ooo',
        'ooo']]
]


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


# Creates the windows class
class createWindow:
    def __init__(self, fontSize, fontColor, buttonColor, x, y, width=None, height=None, text=' '):
        self.fontSize = fontSize
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.fontColor = fontColor
        self.text_rect = None
        self.buttonColor = buttonColor
        self.currentButtonColor = buttonColor
        self.text = text

    # Draws window to screen
    def drawWindow(self, window, padding, autoCenter=False, outline=False, outlineColor=None):
        main_menu_font = pygame.font.SysFont("Arial", self.fontSize)
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
            pygame.draw.rect(window, outlineColor, (text_rect[0] - padding,
                                                    text_rect[1] - padding,
                                                    text_rect[2] + 2 * padding,
                                                    text_rect[3] + 2 * padding))

        self.text_rect = text_rect
        # self.hoveringOverButton()

        pygame.draw.rect(window, self.currentButtonColor, text_rect)

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
        mouse_position = pygame.mouse.get_pos()
        # checks for when mouse is inside the button in the x and y directions.
        if mouse_position[0] > self.text_rect[0] and mouse_position[0] < self.text_rect[0] + self.text_rect[2]:
            if mouse_position[1] > self.text_rect[1] and mouse_position[1] < self.y + self.text_rect[3]:
                # If inside the button do this: Change color of button
                self.currentButtonColor = self.hoveringColor
                # Clicking Code Here
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

    # Draws button to screen
    def drawButton(self, window, padding, autoCenter=False, outline=False, outlineColor=None):
        main_menu_font = pygame.font.SysFont("Arial", self.fontSize)
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
            pygame.draw.rect(window, outlineColor, (text_rect[0] - padding,
                                                    text_rect[1] - padding,
                                                    text_rect[2] + 2 * padding,
                                                    text_rect[3] + 2 * padding))

        self.text_rect = text_rect
        self.hoveringOverButton()

        pygame.draw.rect(window, self.currentButtonColor, text_rect)

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

# Creates Tetris piece class
class tetrisPiece:
    def __init__(self):
        self.x = (gameGridPosX - blockSize + columns // 2 * blockSize)
        self.y = gameGridPosY
        self.bottomCord = gameGridPosY + ((rows-1) * blockSize)
        self.rightCord = gameGridPosX + (columns * blockSize)
        self.rawRotationValue = 0
        self.rotation = 0
        self.shape = random.randint(0, len(blockData) - 1)
        self.color = block_colors[self.shape]
        self.dropCounter = 0

    # places the piece
    def placePiece(self, gridData, dropRate='instant'):
        gridX = (self.x - gameGridPosX) // blockSize
        gridY = (self.y - gameGridPosY) // blockSize
        if dropRate == 'instant':
            while True:
                if self.pieceInDirection('down', 0, None, gridY) is True:
                    break
                else:
                    gridY += 1
        for coordinates in blockData[self.shape][self.rotation]:
            x = coordinates[0]
            y = coordinates[1]
            gridData[gridX + x][gridY + y] = self.color

    # Draws the piece to the screen
    def drawPiece(self, surface, xPos=None, yPos=None):
        # takes the rotation index of the piece that was selected.
        self.rotation = self.rawRotationValue % len(blockData[self.shape])
        if xPos is None:
            xValue = self.x
        else:
            xValue = xPos
        if yPos is None:
            yValue = self.y
        else:
            yValue = yPos
        for coordinates in blockData[self.shape][self.rotation]:
            x = coordinates[0]
            y = coordinates[1]
            # Draws each square of each shape in relation to self.x and self.y position
            pygame.draw.rect(surface, block_colors[self.shape], ((x * blockSize) + xValue, (y * blockSize) + yValue, blockSize, blockSize))

    # checks if the piece is at the bottom of the grid
    def bottomGrid(self):
        bottomGrid = False
        gridX = round((self.x - gameGridPosX) / blockSize)
        gridY = round((self.y - gameGridPosY) / blockSize)
        for coordinates in blockData[self.shape][(self.rawRotationValue) % len(blockData[self.shape])]:
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
        for coordinates in blockData[self.shape][(self.rawRotationValue + 1) % len(blockData[self.shape])]:
            x = coordinates[0] + gridX
            y = coordinates[1] + gridY
            # print(x, y)
            if 0 > x or x > (columns - 1) or y < 0 or y > (rows - 1):
                print('pieceInRotation = true')
                pieceInRotation = True
                return pieceInRotation
            if gridData[x][y] != squareColor:
                pieceInRotation = True

        return pieceInRotation

    # renamed from boundaryCheck to pieceInDirection
    # Checks if there is a piece or the grid edge in the direction of which the piece is moving in
    def pieceInDirection(self, direction, rotation=0, currentPosX=None, currentPosY=None):
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
            for coordinates in blockData[self.shape][(self.rawRotationValue + rotation) % len(blockData[self.shape])]:
                x = coordinates[0] + gridX
                y = coordinates[1] + gridY

                if direction == 'up':
                    if gridData[x][y - 1] != squareColor:
                        pieceInDirection = True
                    if 0 > x or x > (columns - 1) or (y - 1) < 0 or (y - 1) > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
                if direction == 'down':
                    if gridData[x][y + 1] != squareColor:
                        pieceInDirection = True
                    if 0 > x or x > (columns - 1) or (y + 1) < 0 or (y + 1) > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
                if direction == 'left':
                    if gridData[x - 1][y] != squareColor:
                        pieceInDirection = True
                    if 0 > (x - 1) or (x - 1) > (columns - 1) or y < 0 or y > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
                if direction == 'right':
                    if gridData[x + 1][y] != squareColor:
                        pieceInDirection = True
                    if 0 > (x + 1) or (x + 1) > (columns - 1) or y < 0 or y > (rows - 1):
                        pieceInRotation = True
                        return pieceInRotation
        except IndexError:
            pieceInDirection = True
        # print(pieceInDirection)
        return pieceInDirection

    # assist in rotating the piece if there are pieces in the way
    def assistRotate(self):
        rotated = False
        # print('before:', self.rawRotationValue)
        if rotated is False and self.pieceInDirection('down', 1) is False:
            self.rawRotationValue += 1
            self.y += blockSize
            rotated = True

        if rotated is False and self.pieceInDirection('left', 1) is False:
            self.rawRotationValue += 1
            self.x -= blockSize
            rotated = True

        if rotated is False and self.pieceInDirection('right', 1) is False:
            self.rawRotationValue += 1
            self.x += blockSize
            rotated = True

        if rotated is False and self.pieceInDirection('up', 1) is False:
            self.rawRotationValue += 1
            self.y -= blockSize
            rotated = True

    # rotate the piece if allowed
    def rotate(self):
        if self.rotationBoundaryCheck() is False:
            self.rawRotationValue += 1
            self.rotation = self.rawRotationValue % len(blockData[self.shape])
        else:
            self.assistRotate()

    # moves the piece in up direction (used for testing)
    def moveUp(self):
        if (self.y - blockSize) >= gameGridPosY:
            if self.pieceInDirection('up') is False:
                self.y -= blockSize

    # Moves the piece in the down direction
    def moveDown(self):
        pieceInDirection = self.pieceInDirection('down')
        if self.bottomCord >= (self.y + (len(tetris_data[self.shape][self.rotation]) * blockSize)):
            if pieceInDirection is False:
                self.dropCounter = 0
                self.y += blockSize
        return pieceInDirection

    # Moves the tetris piece in the left direction 
    def moveLeft(self):
        if (self.x - blockSize) >= gameGridPosX:
            if self.pieceInDirection('left') is False:
                self.x -= blockSize

    # Moves the tetris piece in the right direction 
    def moveRight(self):
        if (self.x + (len(tetris_data[self.shape][self.rotation][0]) * blockSize)) < self.rightCord:
            if self.pieceInDirection('right') is False:
                self.x += blockSize

    # Checks cords (used for debugging)
    def checkCords(self):
        print(self.x, self.y)
        print(self.rawRotationValue)
        pass

# Convert from custom tetris file to coordinates for (ie how the blocks are placed)
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

# Creates grid that is 10 by 20
def createGrid(rows, columns):
    # change this to grey later
    finishedGrid = []
    finishedGrid = [[squareColor for row in range(rows)] for column in range(columns)]

    return finishedGrid

# Creates grid that is 20 by 10
def createCheckingGrid(rows, columns):
    # change this to grey later
    finishedGrid = []
    finishedGrid = [[squareColor for columns in range(columns)] for row in range(rows)]

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
            pygame.draw.rect(surface, (gridData[column])[row], (startX + (blockSize * column), startY + (blockSize * row), blockSize, blockSize))
    piece.drawPiece(surface)

    # Draws Vertical lines
    for column in range(columns):
        pygame.draw.line(surface, grey, (x, y), (x, y + height), 2)
        x += blockSize

    # Draws Horizontal Lines
    x = startX
    for row in range(rows):
        pygame.draw.line(surface, grey, (x, y), (x + width, y), 2)
        if row == 3:
            pygame.draw.line(surface, red, (x, y), (x + width, y), 3)
        y += blockSize
    y = startY

    # Creates Border
    pygame.draw.rect(surface, darkGrey, (x, y, width, height), 5)

# checks grid and full rows
def checkGrid(gridData, linesCleared):
    running = True
    cleared = linesCleared
    altGridData = createCheckingGrid(rows, columns)
    # Convert from XY to YX format
    for row in range(rows):
        for column in range(columns):
            altGridData[row][column] = gridData[column][row]
    # Checks for full rows and clears them
    for row in range(len(altGridData)):
        filled = True
        for square in altGridData[row]:
            if square == squareColor:
                filled = False
        if filled is True:
            newRow = [squareColor for roww in range(rows)]
            altGridData.pop(row)
            altGridData.insert(0, newRow)
            cleared += 1
        # Ends game when a piece passes the red line
        if row == 2:
            for square in altGridData[row]:
                if square != squareColor:
                    print('GAMEOVER')
                    running = False
    # Convert from YX back to XY format
    for column in range(columns):
        for row in range(rows):
            gridData[column][row] = altGridData[row][column]
    return running, cleared

# updates the stats on the GUI interface
def updateStats(main_window, playerScore, linesCleared, queue, pieceOnHold):
    print(playerScore)
    # Draw the left rect for score and lines cleared
    centerY = window_height / 2 - (440) / 2
    pygame.draw.rect(main_window, grey, (150, centerY, 225, 440))
    pygame.draw.rect(main_window, darkGrey, (150, centerY, 225, 440), 5)
    # shows the player score
    scoreText = createText('Score', 30, white, 220, 330)
    scoreText.drawText(main_window)
    score = createText(str(playerScore), 25, white, 235, 380)
    score.drawText(main_window)
    # shows no of lines cleared
    scoreText = createText('Lines Cleared', 30, white, 170, 475)
    scoreText.drawText(main_window)
    score = createText(str(linesCleared), 25, white, 240, 525)
    score.drawText(main_window)

    # Draw the left rect for queue pieces and pieces on 'hold'
    centerY = window_height / 2 - (750) / 2
    pygame.draw.rect(main_window, grey, (825, centerY, 225, 750))
    pygame.draw.rect(main_window, darkGrey, (825, centerY, 225, 750), 5)\
        # Draws the next pieces
    if len(queue) < 4:
            appendPiece = tetrisPiece()
            queue.append(appendPiece)
    nextText = createText('Next', 30, white, 900, 210)
    nextText.drawText(main_window)
    queue[1].drawPiece(main_window, 900, 270)
    queue[2].drawPiece(main_window, 900, 425)
    # Draws the hold pieces
    holdText = createText('Hold', 30, white, 900, 580)
    holdText.drawText(main_window)

    if pieceOnHold is not None:
        pieceOnHold.drawPiece(main_window, 900, 630)

    pos = pygame.mouse.get_pos()
    print(pos)

    return queue
# main Game loop
def gameLoop(main_window, clock):
    runningState = True
    queue = []
    piece = None
    linesCleared = 0
    placeCountdown = 0
    playerScore = 0
    pieceInDownDirection = False
    numOfPlacedPieces = 0
    numOfPlacedPiecesAtSwap = -1
    pieceOnHold = None
    global gridData
    gridData = createGrid(rows, columns)
    for pieces in range(3):
        appendPiece = tetrisPiece()
        queue.append(appendPiece)
    while runningState:
        playerScore = linesCleared * 100
        if len(queue) < 4:
            appendPiece = tetrisPiece()
            queue.append(appendPiece)
        print(numOfPlacedPieces)
        piece = queue[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                # this key will be changed to
                # up arrow key once prog is finished
                if keys[pygame.K_UP]:
                    piece.rotate()
                    piece = queue[0]
                if keys[pygame.K_SPACE]:
                    piece.placePiece(gridData)
                    numOfPlacedPieces += 1
                    queue.pop(0)
                    piece = queue[0]
                if keys[pygame.K_z]:
                    if numOfPlacedPiecesAtSwap != numOfPlacedPieces:
                        # print("zzzzzzzz")
                        numOfPlacedPiecesAtSwap = numOfPlacedPieces
                        piece.x = (gameGridPosX - blockSize + columns // 2 * blockSize)
                        piece.y = gameGridPosY
                        piece.rotation = 0
                        tempSwapPiece = piece
                        queue.pop(0)
                        if pieceOnHold is not None:
                            queue.insert(0, pieceOnHold)
                            pieceOnHold = tempSwapPiece
                        if pieceOnHold is None:
                            pieceOnHold = tempSwapPiece
        piece = queue[0]

        main_window.fill(lightGrey)
        piece.checkCords()
        drawGrid(main_window, gameGridPosX, gameGridPosY, rows, columns, blockSize, gridData, piece)
        gridX = round((piece.x - gameGridPosX) / blockSize)
        gridY = round((piece.y - gameGridPosY) / blockSize)
        pieceInDownDirection = False
        runningState, linesCleared = checkGrid(gridData, linesCleared)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            if piece.pieceInDirection('down') is False:
                pieceInDownDirection = piece.moveDown()
            else:
                piece.dropCounter = 0
                placeCountdown = 0

        if keys[pygame.K_LEFT]:
            piece.moveLeft()

        if keys[pygame.K_RIGHT]:
            piece.moveRight()

        if piece.dropCounter < FPS:
            piece.dropCounter += (1 + linesCleared * acceleration)
        else:
            pieceInDownDirection = piece.moveDown()
            piece.dropCounter = 0
            if piece.pieceInDirection('down') is False:
                placeCountdown = 0


        if placeCountdown <= FPS*1.75:
            placeCountdown += 1

        if placeCountdown >= FPS*1.75:
            pieceInDownDirection = piece.pieceInDirection('down')
            if pieceInDownDirection is True:
                piece.placePiece(gridData)
                queue.pop(0)
                numOfPlacedPieces += 1
                # piece = tetrisPiece()
                piece = queue[0]
            placeCountDown = 0

        # for i in queue:
        #     for row in tetris_data[i.shape][i.rotation]:
        #         print(row)
        #     print("******************")

        queue = updateStats(main_window, playerScore, linesCleared, queue, pieceOnHold)

        clock.tick(FPS)
        pygame.display.update()
        if runningState is False:
            gameOverScreen(main_window, clock, playerScore)

# Game over screen
def gameOverScreen(main_window, clock, playerScore):
    gameOverContainer = createWindow(30, white, grey, 600, 250, 600, 400)
    gameOverText = createText('GAMEOVER', 110, white, 50, 275)
    scoreText = createText('Score: ' + str(playerScore), 30, white, 220, 425)
    playAgainButton = main_menu_buttons("Play Again", 45, white, green, darkerGreen, 325, 500, lambda: gameLoop(main_window, clock), 250, 100)
    mainMenuButton = main_menu_buttons("Main Menu", 45, white, red, darkerRed, 615, 500, lambda: mainMenu(main_window, clock), 250, 100)

    while True:
        main_window.fill(lightGrey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        print("GAMEOVER")
        gameOverContainer.drawWindow(main_window, 5, True, True, darkGrey)
        gameOverText.drawText(main_window, True)
        scoreText.drawText(main_window, True)
        playAgainButton.drawButton(main_window, 8, False, True, darkGreen)
        mainMenuButton.drawButton(main_window, 8, False, True, darkRed)
        clock.tick(FPS)
        pygame.display.update()

# Create help Window + objects
def helpWindow(main_window, clock):
    # Creates buttons and text
    backButton = main_menu_buttons("Back", 65, white, orange, darkerOrange, 20, 725, lambda: mainMenu(main_window, clock), 200, 100)
    helpContainer = createWindow(30, white, orange, 50, 50, 1100, 800)
    helpTitle = createText('How to play', 75, white, 50, 100)
    body1 = createText('Welcome!', 30, white, 50, 220)
    body2 = createText('The object of the game is to stay alive for as long as possible ', 30, white, 50, 280)
    body3 = createText('and to clear as many lines a possible.', 30, white, 50, 310)
    body4 = createText('To clear a line, you will need to fill an entire row with the ', 30, white, 50, 340)

    body5 = createText('SCORING', 30, white, 50, 395)
    body6 = createText('tetris peices (with no spaces in between).', 30, white, 50, 430)
    body7 = createText('Per line cleared, you get +100 points. The more lines you ', 30, white, 50, 460)
    body8 = createText('clear, the higher your score is!', 30, white, 50, 490)
    body9 = createText('The higher your score, the better you are!', 30, white, 50, 520)

    body10 = createText('GAMEOVER', 30, white, 50, 565)
    body11 = createText('You must not let any Tetris piece go past the red line ', 30, white, 50, 600)
    body12 = createText('otherwise the game will be over', 30, white, 50, 630)
    body13 = createText('Happy Tetrising! ', 30, white, 50, 660)
    
    # Clears screen and writes the text to the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        main_window.fill(lightGrey)
        helpContainer.drawWindow(main_window, 5, True, True, darkOrange)
        backButton.drawButton(main_window, 8, True, True, darkOrange)
        helpTitle.drawText(main_window, True)
        body1.drawText(main_window, True)
        body2.drawText(main_window, True)
        body3.drawText(main_window, True)
        body4.drawText(main_window, True)
        body5.drawText(main_window, True)
        body6.drawText(main_window, True)
        body7.drawText(main_window, True)
        body8.drawText(main_window, True)
        body9.drawText(main_window, True)
        body10.drawText(main_window, True)
        body11.drawText(main_window, True)
        body12.drawText(main_window, True)
        body13.drawText(main_window, True)

        clock.tick(FPS)
        pygame.display.update()

# closes the game
def exitGame(main_window, clock):
    # exitButton = main_menu_buttons("Exit", 100,  white, red, darkerRed, 390, 550, exit, 300, 125)
    while True:
        main_window.fill(lightGrey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        exit()
        # exitButton.drawButton(main_window, 8, True, True, darkRed)
        clock.tick(FPS)
        pygame.display.update()

# creates main Menu with buttons
def mainMenu(main_window, clock):
    pygame.display.set_caption("Main Menu")
    tetris = createText('TETRIS', 100, darkGrey, 390, 35)
    playButton = main_menu_buttons("Play", 70, white, green, darkerGreen, 390, 225, lambda: gameLoop(main_window, clock), 325, 125)
    helpButton = main_menu_buttons("Help", 70, white, orange, darkerOrange, 390, 400, lambda: helpWindow(main_window, clock), 325, 125)
    exitButton = main_menu_buttons("Exit", 70, white, red, darkerRed, 390, 575, lambda: exitGame(main_window, clock), 325, 125)
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

        main_window = pygame.display.set_mode(window_size)
        clock = pygame.time.Clock()
        mainMenu(main_window, clock)

# checks to ensure this TetrisMain.py is the file being run before main program executes
if __name__ == '__main__':
    blockData = convertTetrisData(tetris_data)
    # gridData = createGrid(rows, columns)

    main_loop()
