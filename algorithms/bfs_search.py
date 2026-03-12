# algorithms/bfs_search.py
# Uninformed Search: Breadth-First Search for move generation.
# BFS explores all possible cells level by level without any heuristic.
# Here it is used to generate the complete list of valid moves from a board state.
# It is also called inside MCTS at every node to find legal moves.

from collections import deque
from game.board import EMPTY, BOARD_SIZE
from game.rules import is_valid_move


def bfs_get_valid_moves(board, color):
    """
    Use BFS to find all valid moves for `color` on the given board.

    How it works:
      - Start from every empty cell on the board.
      - Use a queue (FIFO) to visit each empty cell once.
      - Check if placing a piece there is a valid Othello move.
      - Collect and return all valid cells.

    This is 'uninformed' because the order of exploration is purely
    positional (left-to-right, top-to-bottom) with no heuristic guidance.
    """
    valid_moves = []
    visited = set()

    # Seed the queue with every empty cell on the board
    queue = deque()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board.is_empty(r, c):
                queue.append((r, c))

    # BFS loop
    while queue:
        row, col = queue.popleft()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        if is_valid_move(board, row, col, color):
            valid_moves.append((row, col))

    return valid_moves
