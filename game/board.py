# game/board.py
# Handles the 9x9 board state: creating the board, placing pieces, copying state.

EMPTY = 0
BLACK = 1  # AI2 / human when playing black
WHITE = 2  # AI1 / human when playing white

BOARD_SIZE = 9


class Board:
    """Represents the 9x9 Othello board."""

    def __init__(self):
        # Create a 9x9 grid filled with 0 (EMPTY)
        self.grid = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._place_initial_pieces()

    def _place_initial_pieces(self):
        """
        Place the standard Othello starting pieces in the center.
        On a 9x9 board the center is at (4,4).
        Standard 2x2 setup:
            (3,3)=WHITE  (3,4)=BLACK
            (4,3)=BLACK  (4,4)=WHITE
        """
        mid = BOARD_SIZE // 2  # 4
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE

    def place_piece(self, row, col, color):
        """Place a piece of the given color at (row, col)."""
        self.grid[row][col] = color

    def get_piece(self, row, col):
        """Return the piece at (row, col): EMPTY, BLACK, or WHITE."""
        return self.grid[row][col]

    def is_empty(self, row, col):
        """Return True if the cell is empty."""
        return self.grid[row][col] == EMPTY

    def copy(self):
        """Return a deep copy of this board (used by algorithms for simulation)."""
        new_board = Board.__new__(Board)
        new_board.grid = [row[:] for row in self.grid]
        return new_board

    def count(self, color):
        """Count how many pieces of the given color are on the board."""
        return sum(cell == color for row in self.grid for cell in row)

    def get_scores(self):
        """Return a dict with scores for both colors."""
        return {
            BLACK: self.count(BLACK),
            WHITE: self.count(WHITE),
        }

    def is_full(self):
        """Return True if no empty cells remain."""
        return all(cell != EMPTY for row in self.grid for cell in row)

    def print_board(self):
        """Print the board to the console (useful for debugging)."""
        symbols = {EMPTY: ".", BLACK: "B", WHITE: "W"}
        print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
        for r, row in enumerate(self.grid):
            print(str(r) + " " + " ".join(symbols[cell] for cell in row))
        print()
