# ai/white_ai.py
# Student 1 responsibility
# White AI (AI1): uses Minimax with Alpha-Beta pruning,
# combined with heuristic positional scoring and fuzzy logic evaluation.

from ai.base_ai import BaseAI
from algorithms.minimax import get_best_move


class WhiteAI(BaseAI):
    """
    AI1 — plays as WHITE.

    Strategy:
      Minimax with Alpha-Beta pruning + heuristic + fuzzy logic.
      Looks ahead `depth` moves and picks the move with the highest
      combined heuristic+fuzzy evaluation score.
    """

    def __init__(self, color, depth=4):
        """
        color : WHITE (should always be passed as WHITE=2)
        depth : how many moves ahead to search (default 4)
        """
        super().__init__(color)
        self.depth = depth

    def choose_move(self, board):
        """
        Use Minimax (with Alpha-Beta pruning) to select the best move.
        Returns (row, col) or None if no moves are available.
        """
        return get_best_move(board, self.color, self.depth)
