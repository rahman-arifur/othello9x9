# ai/black_ai.py
# Black AI (AI2): uses BFS for move generation + MCTS for decision making.

from ai.base_ai import BaseAI
from algorithms.mcts import mcts_get_best_move


class BlackAI(BaseAI):
    """
    AI2 — plays as BLACK.

    Strategy:
      BFS is called inside MCTS at every node to enumerate valid moves.
      MCTS runs many random game simulations to estimate the best move
      without exhaustively searching the full game tree like Minimax.
    """

    def __init__(self, color, simulations=50):
        """
        color       : BLACK (should always be passed as BLACK=1)
        simulations : number of MCTS playouts per move decision (default 50)
        """
        super().__init__(color)
        self.simulations = simulations

    def choose_move(self, board):
        """
        Use MCTS (with BFS inside for move generation) to select the best move.
        Returns (row, col) or None if no moves are available.
        """
        return mcts_get_best_move(board, self.color, self.simulations)
