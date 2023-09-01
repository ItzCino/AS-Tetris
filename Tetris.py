from Common import *
from Buttons import main_menu_buttons
from Text import createText, blank
from random import randint as randomBlock
from Grid import convertTetrisData, createGrid, drawGrid, checkGrid

from pygame.constants import QUIT
from pygame.draw import rect as draw_rect
from pygame.mouse import get_pos as get_mouse_pos
from pygame.sysfont import SysFont as generate_font

from pygame.display import update as update_display 
from pygame.display import update as refresh_display, set_caption as display_set_caption
from pygame.event import get as get_event_list
from pygame.event import get as get_current_event_list 

from pygame.constants import QUIT, K_UP as up_key, K_DOWN as down_key, K_LEFT as left_key, K_RIGHT as right_key, K_z as z_key, K_SPACE as space_key, KEYDOWN as key_pressed
from pygame.key import get_pressed as get_key_pressed


# Creates Tetris piece class
class TetrisPiece:
    def __init__(self):
        self.x = (gameGridPosX - blockSize + columns // 2 * blockSize)
        self.y = gameGridPosY
        self.bottomCord = gameGridPosY + ((rows-1) * blockSize)
        self.rightCord = gameGridPosX + (columns * blockSize)
        self.rawRotationValue = 0
        self.rotation = 0
        self.shape = randomBlock(0, len(blockData) - 1)
        self.color = block_colors[self.shape]
        self.dropCounter = 0

    # places the piece
    def placePiece(self, dropRate='instant'):
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
            draw_rect(surface, block_colors[self.shape], ((x * blockSize) + xValue, (y * blockSize) + yValue, blockSize, blockSize))

    # checks if the piece is at the bottom of the grid
    def bottomGrid(self, gridData):
        bottomGrid = False
        gridX = round((self.x - gameGridPosX) / blockSize)
        gridY = round((self.y - gameGridPosY) / blockSize)
        for coordinates in blockData[self.shape][(self.rawRotationValue) % len(blockData[self.shape])]:
            x = coordinates[0] + gridX
            y = coordinates[1] + gridY
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
        return pieceInDirection

    # assist in rotating the piece if there are pieces in the way
    def assistRotate(self):
        rotated = False
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


# updates the stats on the GUI interface
def updateStats(main_window, playerScore, linesCleared, queue, pieceOnHold, gameTimer):
    print(playerScore)
    # Draw the left rect for score and lines cleared
    centerY = window_height / 2 - (440) / 2
    draw_rect(main_window, grey, (150, centerY, 225, 440))
    draw_rect(main_window, darkGrey, (150, centerY, 225, 440), 5)
    # shows the time limit
    scoreText = createText('Timer', 30, white, 220, 290)
    scoreText.drawText(main_window, True, 150, 375)
    if gameLength > 0:
        if (gameLength - gameTimer) > 10:
            score = createText(str(gameLength - gameTimer), 25, white, 235, 340)
        if (gameLength - gameTimer) <= 10:
            mod = (gameLength - gameTimer) % 2
            if mod == 0:
                score = createText(str(gameLength - gameTimer), 25, red, 235, 340)
            if mod == 1:
                score = createText(str(gameLength - gameTimer), 25, white, 235, 340)

    if gameLength == 0:
        score = createText(str('∞'), 25, white, 235, 325)
    score.drawText(main_window, True, 150, 375)
    # shows the player score
    scoreText = createText('Score', 30, white, 220, 410)
    scoreText.drawText(main_window, True, 150, 375)
    score = createText(str(playerScore), 25, white, 235, 450)
    score.drawText(main_window, True, 150, 375)
    # shows no of lines cleared
    scoreText = createText('Lines Cleared', 30, white, 170, 530)
    scoreText.drawText(main_window, True, 150, 375)
    score = createText(str(linesCleared), 25, white, 240, 580)
    score.drawText(main_window, True, 150, 375)

    # Draw the left rect for queue pieces and pieces on 'hold'
    centerY = window_height / 2 - (750) / 2
    draw_rect(main_window, grey, (825, centerY, 225, 750))
    draw_rect(main_window, darkGrey, (825, centerY, 225, 750), 5)\
        # Draws the next pieces
    if len(queue) < 4:
            appendPiece = TetrisPiece()
            queue.append(appendPiece)
    nextText = createText('Next', 30, white, 900, 210)
    nextText.drawText(main_window)
    queue[1].drawPiece(main_window, 900, 270)
    if len(queue) < 4:
            appendPiece = TetrisPiece()
            queue.append(appendPiece)
    queue[2].drawPiece(main_window, 900, 425)
    # Draws the hold pieces
    holdText = createText('Hold', 30, white, 900, 580)
    holdText.drawText(main_window)

    if pieceOnHold is not None:
        pieceOnHold.drawPiece(main_window, 900, 630)

    pos = get_mouse_pos()
    print(pos)

    return queue


##### WINDOWS AND MENUS #####

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
        main_menu_font = generate_font("Arial", self.fontSize)
        text_object = main_menu_font.render(self.text, 5, self.fontColor)
        text_rect = text_object.get_rect()
        text_rect.topleft = self.pos

        # Draws background area for Window

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

        draw_rect(window, self.currentButtonColor, text_rect)

        # Centering of text for window
        # Calculates the Topleft position for centering window

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


# creates main Menu with buttons
def mainMenu(main_window, clock):
    global blockData
    blockData = convertTetrisData(tetris_data)
    clock.tick(2)
    display_set_caption("Main Menu")
    tetris = createText('TETRIS', 100, darkGrey, 390, 35)
    playButton = main_menu_buttons("Play", 70, white, green, darkerGreen, 390, 225, lambda: gameLoop(main_window, clock), 325, 125)
    helpButton = main_menu_buttons("Help", 70, white, orange, darkerOrange, 390, 400, lambda: helpMenu(main_window, clock), 325, 125)
    exitButton = main_menu_buttons("Exit", 70, white, red, darkerRed, 390, 575, lambda: exitGameMenu(main_window, clock), 325, 125)
    while True:
        main_window.fill(lightGrey)
        for event in get_current_event_list():
            if event.type == QUIT:
                exit()
        tetris.drawText(main_window, True)
        playButton.drawButton(main_window, 8, True, True, darkGreen)
        helpButton.drawButton(main_window, 8, True, True, darkOrange)
        exitButton.drawButton(main_window, 8, True, True, darkRed)
        clock.tick(FPS)
        refresh_display()


# Create help Window + objects
def helpMenu(main_window, clock):
    # Creates buttons and text
    backButton = main_menu_buttons("Back", 65, white, orange, darkerOrange, 20, 725, lambda: mainMenu(main_window, clock), 200, 100)
    helpContainer = createWindow(30, white, orange, 50, 50, 1100, 800)
    helpTitle = createText('How to play', 75, white, 50, 100)
    body1 = createText('Welcome!', 30, white, 100, 220)
    body2 = createText('The object of the game is to stay alive for as long ', 30, white, 100, 280)
    body3 = createText('as possible and to clear as many lines a possible.', 30, white, 100, 310)
    body4 = createText('To clear a line, you will need to fill an entire row ', 30, white, 100, 340)
    body5 = createText('with the tetris pieces (with no spaces in between).', 30, white, 100, 370)

    body6 = createText('SCORING', 30, white, 100, 420)
    body7 = createText('Per line cleared, you get +100 points. ', 30, white, 100, 460)
    body8 = createText('The more lines you clear, the higher your score is!', 30, white, 100, 490)
    body9 = createText('The higher your score, the better you are!', 30, white, 100, 520)

    body10 = createText('GAMEOVER', 30, white, 100, 565)
    body11 = createText('You must not let any Tetris piece go past the red line ', 30, white, 100, 600)
    body12 = createText('Otherwise the game will be over', 30, white, 100, 630)
    body13 = createText('Happy Tetris - ing! ', 30, white, 100, 660)

    # Creates GUI for Controls

    upKey = main_menu_buttons('↑', 40, darkGrey, lightGrey, lightGrey, 825, 290, blank, 55, 55)
    upKeyText = createText('Rotate piece', 25, white, 905, 300)

    downKey = main_menu_buttons('↓', 40, darkGrey, lightGrey, lightGrey, 825, 360, blank, 55, 55)
    downKeyText = createText('Move Piece Down', 25, white, 905, 370)

    leftKey = main_menu_buttons('←', 40, darkGrey, lightGrey, lightGrey, 825, 430, blank, 55, 55)
    leftKeyText = createText('Move Piece left', 25, white, 905, 440)

    rightKey = main_menu_buttons('→', 40, darkGrey, lightGrey, lightGrey, 825, 500, blank, 55, 55)
    rightKeyText = createText('Move Piece right', 25, white, 905, 510)

    zKey = main_menu_buttons('Z', 40, darkGrey, lightGrey, lightGrey, 825, 570, blank, 55, 55)
    zKeyText = createText('Hold Piece', 25, white, 905, 580)

    spacebar = main_menu_buttons('Spacebar', 40, darkGrey, lightGrey, lightGrey, 855, 725, blank, 225, 55)
    spacebarText = createText('Drop Piece', 25, white, 905, 675)

    # Clears screen and writes the text to the screen
    while True:
        print()

        for event in get_current_event_list():
            if event.type == QUIT:
                exit()
        main_window.fill(lightGrey)
        helpContainer.drawWindow(main_window, 5, True, True, darkOrange)
        backButton.drawButton(main_window, 8, True, True, darkOrange)
        helpTitle.drawText(main_window, True)
        body1.drawText(main_window)
        body2.drawText(main_window)
        body3.drawText(main_window)
        body4.drawText(main_window)
        body5.drawText(main_window)
        body6.drawText(main_window)
        body7.drawText(main_window)
        body8.drawText(main_window)
        body9.drawText(main_window)
        body10.drawText(main_window)
        body11.drawText(main_window)
        body12.drawText(main_window)
        body13.drawText(main_window)

        upKey.drawButton(main_window, 5, False, True, darkGrey)
        upKeyText.drawText(main_window)
        downKey.drawButton(main_window, 5, False, True, darkGrey)
        downKeyText.drawText(main_window)
        leftKey.drawButton(main_window, 5, False, True, darkGrey)
        leftKeyText.drawText(main_window)
        rightKey.drawButton(main_window, 5, False, True, darkGrey)
        rightKeyText.drawText(main_window)
        spacebar.drawButton(main_window, 5, False, True, darkGrey)
        spacebarText.drawText(main_window)
        zKey.drawButton(main_window, 5, False, True, darkGrey)
        zKeyText.drawText(main_window)
        clock.tick(FPS)
        refresh_display()


# Game over menu
def gameOverMenu(main_window, clock, playerScore):

    scores, data = parseLeaderboards(playerScore, gameLength)

    centerY = window_height / 2 - (400) / 2
    leaderboardsContainer = createWindow(30, white, grey, 75, centerY, 250, 400)
    leaderboardsText = createText('Top 8 Leaderboards', 25, white, 75, 290)
    leaderboardScoreText = createText('Score:', 25, white, 75, 335)
    leaderboardTimelimitText = createText('Time Limit:', 25, white, 75, 335)

    gameOverContainer = createWindow(30, white, grey, 400, 250, 600, 400)
    gameOverText = createText('GAMEOVER', 95, white, 400, 275)
    scoreText = createText('Score: ' + str(playerScore), 30, white, 470, 425)
    playAgainButton = main_menu_buttons("Play Again", 45, white, green, darkerGreen, 435, 500, lambda: gameLoop(main_window, clock), 250, 100)
    mainMenuButton = main_menu_buttons("Main Menu", 45, white, red, darkerRed, 715, 500, lambda: mainMenu(main_window, clock), 250, 100)

    highScoreText = createText('NEW HIGH SCORE!', 25, red, 470, 385)

    while True:
        textColor = white
        startY = 375
        highScore = False
        main_window.fill(lightGrey)
        for event in get_current_event_list():
            if event.type == QUIT:
                exit()
        gameOverContainer.drawWindow(main_window, 5, False, True, darkGrey)
        gameOverText.drawText(main_window, True, 400, 1000)
        scoreText.drawText(main_window, True, 400, 1000)
        playAgainButton.drawButton(main_window, 8, False, True, darkGreen)
        mainMenuButton.drawButton(main_window, 8, False, True, darkRed)

        leaderboardsContainer.drawWindow(main_window, 5, False, True, darkGrey)
        leaderboardsText.drawText(main_window, True, 75, 325)
        leaderboardScoreText.drawText(main_window, True, 105, 180)
        leaderboardTimelimitText.drawText(main_window, True, 180, 325)

        for num in range(0, len(scores)):
            textColor = white
            if playerScore == scores[num] and highScore is False:
                highScore = True
                textColor = red
                highScoreText.drawText(main_window, True, 400, 1000)
            score = createText(str(scores[num]), 25, textColor, 180-(13*len(str(scores[num]))), startY+(num*30))
            score.drawText(main_window, False, 75, 180)
            if data[scores[num]] == 0:
                timeLimit = createText('∞', 25, textColor, 180, startY+(num*30))
                timeLimit.drawText(main_window, True, 180, 325)
            else:
                timeLimit = createText(str(data[scores[num]]), 25, textColor, 180, startY+(num*30))
                timeLimit.drawText(main_window, True, 180, 325)

        clock.tick(FPS)
        refresh_display()



# Opens Exit menu the game
def exitGameMenu(main_window, clock):
    # Creates the text and button objects
    gameOverContainer = createWindow(30, white, grey, 575, 250, 650, 400)
    exitGameText = createText('Exit Game?', 95, white, 50, 300)
    playAgainButton = main_menu_buttons("Yes", 45, white, green, darkerGreen,
                                        325, 475, exit, 250, 100)
    mainMenuButton = main_menu_buttons("No", 45, white, red, darkerRed, 615, 475, lambda: mainMenu(main_window, clock), 250, 100)
    while True:
        # Draws the buttons and windows + check for button clicks
        main_window.fill(lightGrey)
        for event in get_current_event_list():
            if event.type == QUIT:
                exit()
        gameOverContainer.drawWindow(main_window, 5, True, True, darkGrey)
        exitGameText.drawText(main_window, True)
        playAgainButton.drawButton(main_window, 8, False, True, darkGreen)
        mainMenuButton.drawButton(main_window, 8, False, True, darkRed)
        clock.tick(FPS)
        refresh_display()

# main Game loop
def gameLoop(main_window, clock):
    # initialize game
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
    varGameTimer = 0
    gameTimer = 0
    # stores current game data from the playing grid
    global gridData
    gridData = createGrid(rows, columns)
    for pieces in range(3):
        appendPiece = TetrisPiece()
        queue.append(appendPiece)
    # game loop
    while runningState:
        # scoring
        playerScore = (numOfPlacedPieces * 100) + (linesCleared * 450)
        # random selection of pieces and sets up queue of size 3
        if len(queue) < 4:
            appendPiece = TetrisPiece()
            queue.append(appendPiece)
        print(numOfPlacedPieces)
        piece = queue[0]
        # listens for key inputs
        for event in get_event_list ():
            # quits game if exit is pressed
            if event == QUIT:
                exit()
            # listens for key inputs
            if event.type == key_pressed:
                keys = get_key_pressed()
                # rotates pieces
                if keys[up_key]:
                    piece.rotate()
                    piece = queue[0]
                # instantly drops pieces to the bottom
                if keys[space_key]:
                    piece.placePiece()
                    numOfPlacedPieces += 1
                    queue.pop(0)
                    piece = queue[0]
                # temporarily holds pieces
                if keys[z_key]:
                    if numOfPlacedPiecesAtSwap != numOfPlacedPieces:
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
        # selects the next piece in queue
        piece = queue[0]
        keys = get_key_pressed()

        # checks if the down arrow is pressed if so then move piece down
        if keys[down_key]:
            if piece.pieceInDirection('down') is False:
                pieceInDownDirection = piece.moveDown()
            if piece.pieceInDirection('down') is True:
                piece.dropCounter = 0
                placeCountdown = 0

        # checks if the left arrow is pressed if so then move piece left
        if keys[left_key]:
            piece.moveLeft()
        # checks if the right arrow is pressed if so then move piece right
        if keys[right_key]:
            piece.moveRight()

        if piece.dropCounter < FPS:
            piece.dropCounter += (1 + linesCleared * acceleration)
        else:
            pieceInDownDirection = piece.moveDown()
            piece.dropCounter = 0
            if piece.pieceInDirection('down') is False:
                placeCountdown = 0

        # game tick/timer between each time the piece moves
        if varGameTimer < FPS:
            varGameTimer += 1
        else:
            varGameTimer = 0
            gameTimer += 1
            if gameTimer == gameLength:
                gameOverMenu(main_window, clock, playerScore)

        if placeCountdown <= FPS*1.75:
            placeCountdown += 1

        if placeCountdown >= FPS*1.75:
            pieceInDownDirection = piece.pieceInDirection('down')
            if pieceInDownDirection is True:
                piece.placePiece()
                queue.pop(0)
                numOfPlacedPieces += 1
                piece = queue[0]
            placeCountDown = 0

        main_window.fill(lightGrey)
        piece.checkCords()
        drawGrid(main_window, gameGridPosX, gameGridPosY, rows, columns, blockSize, gridData, piece)
        gridX = round((piece.x - gameGridPosX) / blockSize)
        gridY = round((piece.y - gameGridPosY) / blockSize)
        pieceInDownDirection = False
        runningState, linesCleared = checkGrid(gridData, linesCleared)

        queue = updateStats(main_window, playerScore, linesCleared, queue, pieceOnHold, gameTimer)

        clock.tick(FPS)
        update_display()
        if runningState is False:
            gameOverMenu(main_window, clock, playerScore)

# Updates the leadboards and reads and write data to the leaderboards.
def parseLeaderboards(playerScore, gameLength):
    data = {}
    dataList = []
    tempDataList = []

    # Writes latest score
    leaderboardFile = open('Leaderboards_' + str(gameLength) + '_Seconds.txt', 'a+')
    leaderboardFile.write('{}:{}\n'.format(playerScore, gameLength))
    leaderboardFile = open('Leaderboards_' + str(gameLength) + '_Seconds.txt', 'r')

    # Stores scores in a temp list
    lines = leaderboardFile.read().split()
    for line in lines:
        if len(line) <= 1:
            pass
        lineList = line.split(':')
        score = int(lineList[0])
        data[score] = int(lineList[1])
        tempDataList.append(score)
    tempDataList.sort()
    tempDataList.reverse()

    # Gets top 8 scores
    for value in range(0, len(tempDataList)):
        if len(dataList) < 8:
            dataList.append(tempDataList[value])

    leaderboardFile = open('Leaderboards_' + str(gameLength) + '_Seconds.txt', 'w')
    leaderboardFile = open('Leaderboards_' + str(gameLength) + '_Seconds.txt', 'a+')

    # Writes top 8 scores to leaderboardFile
    for value in range(0, len(dataList)):
        leaderboardFile.write('{}:{}\n'.format(dataList[value], data[dataList[value]]))
        print(dataList[value], data[dataList[value]])
    leaderboardFile.close()

    return dataList, data