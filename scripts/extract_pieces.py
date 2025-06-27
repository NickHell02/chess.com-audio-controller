#######################################
#
#    Script to auto generate images
#      for piece recognition
#
#                 by
#
#          Code Monkey King
#
#######################################

# Adapted for chess.com currently setup for analysis mode but correctly extracts the pieces on the white squares

# Set this FEN on the chess board in the browser:
# "k1q1r1b1/1n1p4/8/8/8/1N1P4/K1Q1R1B1/8 w - - 0 1"
# to make sure the script would work properly

# packages
import cv2
import pyautogui as pg
import numpy as np

# constants (modify if needed)
BOARD_SIZE = 616
DARK_SQUARE_THRESHOLD = 185
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 226
BOARD_LEFT_COORD = 226

# map pieces
piece_names = {
    '0': 'black_king',
    '1': 'black_queen',
    '2': 'black_rook',
    '3': 'black_bishop',
    '4': 'black_knight',
    '5': 'black_pawn',
    '6': 'white_knight',
    '7': 'white_pawn',
    '8': 'white_king',
    '9': 'white_queen',
    '10': 'white_rook',
    '11': 'white_bishop'
}

# board top left corner coords (change if needed)

# take a screenshot and store it locally
screenshot_image_object = pg.screenshot('screenshot.png', region=(BOARD_LEFT_COORD, BOARD_TOP_COORD, BOARD_SIZE, BOARD_SIZE))

# load local screenshot
screenshot = cv2.cvtColor(np.array(screenshot_image_object), cv2.COLOR_RGB2BGR)

# convert screenshot to grayscale
screenshot_grayscale = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# piece code
piece_code = 0

y = 0

# loop over board rows
for row in range(8):

    x = 0
    # loop over board columns
    for col in range(8):
        # pick up certain rows
        brightness = screenshot_grayscale[y][x]
        print(f"Square ({row},{col}) has brightness: {brightness}")
        if row in [0, 1, 5, 6]:
            # match only light squares
            if screenshot_grayscale[y][x] > DARK_SQUARE_THRESHOLD:
                # skip empty cells
                if row == 1 and col < 4: continue
                if row == 5 and col < 4: continue

                # crop piece image
                piece_image = screenshot[y:y + CELL_SIZE, x: x + CELL_SIZE]

                # uncomment to display extracted images
                #cv2.imshow('scr', piece_image)
                #cv2.waitKey(0)

                # store extracted image
                cv2.imwrite('./pieces/' + piece_names[str(piece_code)] + '.png', piece_image)
                print(f"Processing: {piece_names[str(piece_code)]}")

                # increment piece code
                piece_code += 1

        # increment x coord by cell size
        x += CELL_SIZE

    # restore x coord, increment y coordinate by cell size
    x = 0
    y += CELL_SIZE

# clean up windows
cv2.destroyAllWindows()