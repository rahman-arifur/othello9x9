# ai/human_player.py
# Represents a human player. Unlike AI players, the human does not have
# a choose_move() that computes a move — instead they click the board.
# This class stores the pending move submitted via the web interface
# and validates it before applying it to the board.

from game.rules import is_valid_move


class HumanPlayer:
    """
    Represents a human player in the game.
    The human submits moves by clicking cells on the board.
    The Flask route calls submit_move() when a click is received,
    and the game manager calls get_move() to retrieve it.
    """

    def __init__(self, color):
        """
        color: the piece color the human is playing (BLACK=1 or WHITE=2).
        """
        self.color = color
        self._pending_move = None  # (row, col) waiting to be consumed

    def submit_move(self, row, col, board):
        """
        Called by the Flask route when the human clicks a cell.
        Validates the move before storing it.
        Returns True if the move is valid and was accepted, False otherwise.
        """
        if is_valid_move(board, row, col, self.color):
            self._pending_move = (row, col)
            return True
        return False

    def has_pending_move(self):
        """Return True if a valid move is waiting to be consumed."""
        return self._pending_move is not None

    def choose_move(self, board):
        """
        Return the pending human move and clear it.
        Returns None if no move has been submitted yet.
        The game manager calls this on the human player's turn.
        """
        move = self._pending_move
        self._pending_move = None
        return move

    def clear_move(self):
        """Discard any pending move (e.g., when restarting the game)."""
        self._pending_move = None
