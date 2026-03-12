# game/rules.py
# Student 2 responsibility
# Handles Othello rule logic: valid move checking and piece flipping.

from game.board import EMPTY, BLACK, WHITE, BOARD_SIZE

# All 8 directions a piece can affect: (row_delta, col_delta)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0,  -1),          (0,  1),
              (1,  -1),  (1, 0), (1,  1)]


def opponent(color):
    """Return the opponent's color."""
    return WHITE if color == BLACK else BLACK


def is_valid_move(board, row, col, color):
    """
    Return True if placing a piece of `color` at (row, col) is a legal move.
    A move is legal if:
      1. The cell is empty.
      2. At least one opponent piece is flipped as a result.
    """
    if not board.is_empty(row, col):
        return False
    return len(_get_flipped_pieces(board, row, col, color)) > 0


def get_valid_moves(board, color):
    """
    Return a list of (row, col) tuples representing all legal moves
    for `color` on the given board.
    """
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if is_valid_move(board, r, c, color):
                moves.append((r, c))
    return moves


def apply_move(board, row, col, color):
    """
    Apply a move: place the piece and flip all opponent pieces that are
    now sandwiched. Modifies the board in place.
    Returns the list of flipped positions (useful for animation/undo).
    """
    flipped = _get_flipped_pieces(board, row, col, color)
    board.place_piece(row, col, color)
    for (r, c) in flipped:
        board.place_piece(r, c, color)
    return flipped


def _get_flipped_pieces(board, row, col, color):
    """
    Internal helper. Returns all (row, col) positions that would be flipped
    if `color` plays at (row, col). Returns an empty list if no flips occur.
    """
    opp = opponent(color)
    all_flipped = []

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        candidates = []  # pieces that might get flipped in this direction

        # Walk in the direction while we see opponent pieces
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board.get_piece(r, c) == opp:
            candidates.append((r, c))
            r += dr
            c += dc

        # If the line ends with one of our own pieces, the candidates are flipped
        if candidates and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board.get_piece(r, c) == color:
            all_flipped.extend(candidates)

    return all_flipped


def has_valid_moves(board, color):
    """Return True if `color` has at least one valid move."""
    return len(get_valid_moves(board, color)) > 0


def is_game_over(board):
    """
    The game is over when:
      - Neither player has any valid moves, OR
      - The board is completely full.
    """
    if board.is_full():
        return True
    if not has_valid_moves(board, BLACK) and not has_valid_moves(board, WHITE):
        return True
    return False


def get_winner(board):
    """
    Return the color of the winner (BLACK or WHITE).
    Since draws are impossible on a 9x9 board, this always returns a winner.
    """
    scores = board.get_scores()
    if scores[BLACK] > scores[WHITE]:
        return BLACK
    return WHITE
