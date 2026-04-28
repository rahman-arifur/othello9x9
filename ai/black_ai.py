# ai/black_ai.py
# Black AI (AI2): uses BFS for move generation + MCTS for decision making.

from ai.base_ai import BaseAI
from algorithms.mcts import mcts_get_best_move
import time


class BlackAI(BaseAI):
    """
    start = time.perf_counter()
    try:
      move = mcts_get_best_move(board, self.color, self.simulations, time_budget=self.time_limit)
    except Exception:
      move = mcts_get_best_move(board, self.color, self.simulations)
    elapsed = time.perf_counter() - start
    if self.time_limit is not None and elapsed < self.time_limit:
      time.sleep(self.time_limit - elapsed)
    return move
      MCTS runs many random game simulations to estimate the best move
      without exhaustively searching the full game tree like Minimax.
    """

    def __init__(self, color, simulations=50, time_limit=None):
        """
        color       : BLACK (should always be passed as BLACK=1)
        simulations : number of MCTS playouts per move decision (default 50)
        """
        super().__init__(color)
        self.simulations = simulations
        # time_limit: maximum seconds allowed per move (None = use fixed simulations)
        self.time_limit = time_limit

    def choose_move(self, board):
        """
        Use MCTS (with BFS inside for move generation) to select the best move.
        Returns (row, col) or None if no moves are available.
        """
        try:
          return mcts_get_best_move(board, self.color, self.simulations, time_budget=self.time_limit)
        except Exception:
          return mcts_get_best_move(board, self.color, self.simulations)
