import pyautogui as pg
import cv2 as cv
import numpy as np
import os
import pprint

# --- Constants ---
BOARD_SIZE = 616
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 226
BOARD_LEFT_COORD = 226
PIECES_DIRECTORY = 'pieces_white'
CONFIDENCE = 0.8

piece_names = [
    'white_pawn', 'white_knight', 'white_bishop', 'white_rook', 'white_queen', 'white_king',
    'black_pawn', 'black_knight', 'black_bishop', 'black_rook', 'black_queen', 'black_king'
]
row_codes = {
    0 : 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
}


def extract_cell_by_cell():
    screenshot_image_object = pg.screenshot('screenshot.png',
                                            region=(BOARD_LEFT_COORD, BOARD_TOP_COORD, BOARD_SIZE, BOARD_SIZE))
    screenshot = cv.cvtColor(np.array(screenshot_image_object), cv.COLOR_RGB2BGR)

    print("Board screenshot taken. Now analyzing cell by cell")
    dimensions = CELL_SIZE

    # Loop through each cell image
    y = 0
    for row in range(8):
        x = 0
        for col in range(8):
            cell_image = screenshot[y:y + CELL_SIZE, x: x + CELL_SIZE]

            cv.imwrite('./cells/' + row_codes[col] + str(8 - row) + '.png', cell_image)
            print(f"Processing: {row_codes[col] + str(8 - row)}")
            x += dimensions
        x = 0
        y += dimensions

# --- Main Execution ---
if __name__ == "__main__":

    print("\n--- Detected Position ---")
    extract_cell_by_cell()
    print("-------------------------")