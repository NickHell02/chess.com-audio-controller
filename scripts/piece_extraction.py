import pyautogui as pg
import cv2 as cv
import numpy as np
import os
import pprint

# --- Constants ---
BOARD_TOP_COORD = 225
BOARD_LEFT_COORD = 225
BOARD_SIZE = 616
CELL_SIZE = BOARD_SIZE / 8
PIECES_DIRECTORY = 'chess_pieces'
CONFIDENCE = 0.3

piece_names = [
    'white_pawn', 'white_knight', 'white_bishop', 'white_rook', 'white_queen', 'white_king',
    'black_pawn', 'black_knight', 'black_bishop', 'black_rook', 'black_queen', 'black_king'
]

def pixel_to_chess_notation(pixel_x, pixel_y, board_left, board_top, cell_size):
    """Converts a pixel coordinate (x, y) to a chess square notation (e.g., 'e4')."""
    # Adjust coordinates to be relative to the board's top-left corner
    rel_x = pixel_x - board_left
    rel_y = pixel_y - board_top

    # Calculate column and row index
    col = int(rel_x // cell_size)
    row = 7 - int(rel_y // cell_size)  # 7-row because board coordinates start from top (row 8)

    # Convert to chess notation
    files = 'abcdefgh'
    ranks = '12345678'

    if 0 <= col < 8 and 0 <= row < 8:
        return f"{files[col]}{ranks[row]}"
    else:
        return None


def recognize_position():
    piece_locations = {name: [] for name in piece_names}
    all_found_centers = []  # Helper list to prevent duplicate detections

    screenshot = pg.screenshot(region=(BOARD_LEFT_COORD, BOARD_TOP_COORD, BOARD_SIZE, BOARD_SIZE))
    screenshot.save('board_screenshot.png')

    print("Board screenshot taken. Now locating pieces...")

    # Loop through each piece image
    for piece_name in piece_names:
            # Correctly build the full path to the piece image
            piece_path = os.path.join(PIECES_DIRECTORY, piece_name + '.png')

            print(f'Current piece path: {piece_path}')

            if not os.path.exists(piece_path):
                print(f"Warning: Piece image not found at {piece_path}")
                continue

            # Search for the piece WITHIN the screenshot image, not the whole screen
            locations = pg.locateAllOnScreen(piece_path, confidence=CONFIDENCE,
                                             region=(BOARD_LEFT_COORD, BOARD_TOP_COORD, BOARD_SIZE, BOARD_SIZE))

            print(len(list(locations)))
            for loc in locations:
                center_point = pg.center(loc)
                # Denoise: Check if this piece is too close to an already found one
                is_duplicate = False
                for existing_center in all_found_centers:
                    distance = np.sqrt(
                        (center_point.x - existing_center.x) ** 2 + (center_point.y - existing_center.y) ** 2)
                    if distance < CELL_SIZE / 2:  # If centers are closer than half a cell, it's a duplicate
                        is_duplicate = True
                        break

                if not is_duplicate:
                    # Convert pixel location to chess notation
                    chess_square = pixel_to_chess_notation(center_point.x, center_point.y, BOARD_LEFT_COORD,
                                                           BOARD_TOP_COORD, CELL_SIZE)
                    if chess_square:
                        piece_locations[piece_name].append(chess_square)
                        all_found_centers.append(center_point)

    return piece_locations


# --- Main Execution ---
if __name__ == "__main__":
    print("Starting chess position recognition...")
    current_position = recognize_position()

    print("\n--- Detected Position ---")
    pprint.pprint(current_position)
    print("-------------------------")