# ai/white_ai.py
# Student 1 responsibility
# White AI (AI1): uses Minimax with Alpha-Beta pruning,
# combined with heuristic positional scoring and fuzzy logic evaluation.

from ai.base_ai import BaseAI
from algorithms.minimax import get_best_move
import time


class WhiteAI(BaseAI):
    """
    AI1 — plays as WHITE.

    Strategy:
      Minimax with Alpha-Beta pruning + heuristic + fuzzy logic.
      Looks ahead `depth` moves and picks the move with the highest
      combined heuristic+fuzzy evaluation score.
    """

    def __init__(self, color, depth=4, time_limit=None):
        """
        color : WHITE (should always be passed as WHITE=2)
        depth : how many moves ahead to search (default 4)
        """
        super().__init__(color)
        self.depth = depth
        # time_limit: maximum seconds allowed per move (None = no limit)
        self.time_limit = time_limit

    def choose_move(self, board):
        """
        Use Minimax (with Alpha-Beta pruning) to select the best move.
        Returns (row, col) or None if no moves are available.
        """
        start = time.perf_counter()
        try:
          move = get_best_move(board, self.color, self.depth, time_budget=self.time_limit)
        except Exception:
          # If something goes wrong with timing, fall back to non-timed call
          move = get_best_move(board, self.color, self.depth)
        elapsed = time.perf_counter() - start
        # Enforce minimum duration equal to the configured time limit
        if self.time_limit is not None and elapsed < self.time_limit:
          time.sleep(self.time_limit - elapsed)
        return move
