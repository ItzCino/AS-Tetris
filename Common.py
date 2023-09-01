# Common data

acceleration = 0.2
gameLength = 0  # Sets the length of the game (in seconds). Set to value to 0 for NO time limit

FPS = 15

window_width = 1200
window_height = 900
window_size = (window_width, window_height)

linesCleared = 0
gameGridPosX = 425
gameGridPosY = 50
blockSize = 35
columns = 10
rows = 23

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

# Sets the default square color
squareColor = black

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
      'oo']]
]