# algorithms/fuzzy_logic.py
# Student 1 responsibility
# Fuzzy Logic: assigns qualitative labels to board positions and converts
# them into numeric scores for the White AI evaluation.
#
# Fuzzy logic uses linguistic rules rather than exact numbers:
#   "If the piece is in a corner, its value is VERY GOOD."
#   "If the piece is on an edge, its value is GOOD."
#   "If the piece is in the center, its value is NEUTRAL."
# These labels are then mapped to crisp numeric values (defuzzification).

from game.board import BOARD_SIZE, BLACK, WHITE

# --- Fuzzy membership definitions ---
# Each cell belongs to a fuzzy category based on its position.

# Corner cells
CORNERS = {(0, 0), (0, 8), (8, 0), (8, 8)}

# Edge cells (border but not corner)
def _is_edge(r, c):
    return (r == 0 or r == BOARD_SIZE - 1 or
            c == 0 or c == BOARD_SIZE - 1) and (r, c) not in CORNERS


# --- Fuzzy labels ---
VERY_GOOD  = "very_good"
GOOD       = "good"
NEUTRAL    = "neutral"
BAD        = "bad"
VERY_BAD   = "very_bad"

# --- Crisp values for each fuzzy label (defuzzification) ---
CRISP_VALUES = {
    VERY_GOOD:  10,
    GOOD:        5,
    NEUTRAL:     1,
    BAD:        -5,
    VERY_BAD:  -10,
}

# Cells adjacent to corners are BAD to occupy early (they give opponent corners)
CORNER_ADJACENT = {
    (0, 1), (1, 0), (1, 1),   # adjacent to (0,0)
    (0, 7), (1, 7), (1, 8),   # adjacent to (0,8)
    (7, 0), (8, 1), (7, 1),   # adjacent to (8,0)
    (7, 7), (7, 8), (8, 7),   # adjacent to (8,8)
}


def get_fuzzy_label(row, col):
    """
    Return the fuzzy linguistic label for a board position.
    Rules (in priority order):
      - Corner          → VERY_GOOD
      - Corner-adjacent → VERY_BAD  (giving opponent a corner is dangerous)
      - Edge            → GOOD
      - Otherwise       → NEUTRAL
    """
    if (row, col) in CORNERS:
        return VERY_GOOD
    if (row, col) in CORNER_ADJACENT:
        return VERY_BAD
    if _is_edge(row, col):
        return GOOD
    return NEUTRAL


def fuzzy_score(row, col):
    """
    Return the crisp numeric score for a position using fuzzy defuzzification.
    """
    label = get_fuzzy_label(row, col)
    return CRISP_VALUES[label]


def fuzzy_evaluate_board(board, color):
    """
    Evaluate the entire board using fuzzy logic.
    Sum up the fuzzy scores of all pieces:
      - Our pieces contribute positively.
      - Opponent pieces contribute negatively.
    """
    opp = WHITE if color == BLACK else BLACK
    score = 0

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board.get_piece(r, c)
            if piece == color:
                score += fuzzy_score(r, c)
            elif piece == opp:
                score -= fuzzy_score(r, c)

    return score
