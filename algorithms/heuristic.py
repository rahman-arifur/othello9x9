# algorithms/heuristic.py
# Informed Search: positional heuristic that scores the board for White AI.
#
# The evaluation gives higher scores to more strategically valuable positions.
# Corners are the most valuable because they cannot be flipped.
# Edges are good because they are harder to surround.
# Center positions are neutral.

from game.board import BOARD_SIZE, BLACK, WHITE

# --- Positional weight table for a 9x9 board ---
# Each cell gets a score based on how strategically important it is.
# Positive = good for the evaluated player.
POSITION_WEIGHTS = [
    [100, -20, 10,  5,  5, 10, -20, 100,  100],
    [-20, -40, -5, -5, -5, -5, -40, -20,  -20],
    [ 10,  -5,  1,  1,  1,  1,  -5,  10,   10],
    [  5,  -5,  1,  1,  1,  1,  -5,   5,    5],
    [  5,  -5,  1,  1,  1,  1,  -5,   5,    5],
    [  5,  -5,  1,  1,  1,  1,  -5,   5,    5],
    [ 10,  -5,  1,  1,  1,  1,  -5,  10,   10],
    [-20, -40, -5, -5, -5, -5, -40, -20,  -20],
    [100, -20, 10,  5,  5, 10, -20, -20,  100],
]


def evaluate_board(board, color):
    """
    Score the board from the perspective of `color`.
    A higher score means the board is better for `color`.

    The evaluation sums up the positional weights of all pieces:
      - Our pieces add to the score.
      - Opponent pieces subtract from the score.
    """
    opp = WHITE if color == BLACK else BLACK
    score = 0

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board.get_piece(r, c)
            if piece == color:
                score += POSITION_WEIGHTS[r][c]
            elif piece == opp:
                score -= POSITION_WEIGHTS[r][c]

    return score


def get_position_value(row, col):
    """
    Return the raw positional weight of a single cell.
    Used by fuzzy logic and Minimax for quick lookups.
    """
    return POSITION_WEIGHTS[row][col]
