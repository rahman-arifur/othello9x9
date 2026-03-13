# ai/base_ai.py
# Shared base class that both AI players inherit from.
# Defines the interface every AI must implement: choose_move().

class BaseAI:
    """
    Abstract base class for all AI players.
    Subclasses must implement the choose_move() method.
    """

    def __init__(self, color):
        """
        color: the piece color this AI controls (BLACK=1 or WHITE=2).
        """
        self.color = color

    def choose_move(self, board):
        """
        Given the current board state, return the best move as (row, col).
        Must be overridden by every subclass.
        Returns None if no valid moves are available.
        """
        raise NotImplementedError("Subclasses must implement choose_move()")
