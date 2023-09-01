from Common import rows, columns, squareColor, grey, darkGrey, red
from pygame.draw import rect as draw_rect, line as draw_line


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
            draw_rect(surface, (gridData[column])[row], (startX + (blockSize * column), startY + (blockSize * row), blockSize, blockSize))
    piece.drawPiece(surface)

    # Draws Vertical lines
    for column in range(columns):
        draw_line(surface, grey, (x, y), (x, y + height), 2)
        x += blockSize

    # Draws Horizontal Lines
    x = startX
    for row in range(rows):
        draw_line(surface, grey, (x, y), (x + width, y), 2)
        if row == 3:
            draw_line(surface, red, (x, y), (x + width, y), 3)
        y += blockSize
    y = startY

    # Creates Border
    draw_rect(surface, darkGrey, (x, y, width, height), 5)


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


