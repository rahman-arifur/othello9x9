# algorithms/mcts.py
# Monte Carlo Tree Search (MCTS) for the Black AI.
#
# Instead of exhaustively searching like Minimax, MCTS runs many random
# game simulations ("playouts") to estimate which moves lead to victory.
#
# The four steps:
#   1. Selection   - Walk the tree picking nodes with the best UCB1 score.
#   2. Expansion   - Add a new unvisited child to the selected node.
#   3. Simulation  - Play a heuristic-guided game to the end from that node.
#   4. Backprop    - Propagate the win/loss result back up the tree.
#
# BFS (from bfs_search.py) is used at every node to generate valid moves.
# The heuristic (from heuristic.py) guides move selection during simulation
# so rollouts favour strategically strong positions rather than playing blindly.

import math
import random

from game.board import BLACK, WHITE, BOARD_SIZE
from game.rules import apply_move, is_game_over, has_valid_moves, get_valid_moves
from algorithms.bfs_search import bfs_get_valid_moves
from algorithms.heuristic import POSITION_WEIGHTS

# How many simulations to run per move decision.
# 50 gives fast response (~0.7s) while still being competitive.
SIMULATIONS = 50

# Exploration constant for UCB1. Higher = more exploration.
UCB1_C = math.sqrt(2)


class MCTSNode:
    """
    Represents one node in the MCTS game tree.
    Each node stores a board state, whose turn it is, and statistics.
    """

    def __init__(self, board, color, parent=None, move=None):
        self.board = board          # Board state at this node
        self.color = color          # Color to move at this node
        self.parent = parent        # Parent node (None for root)
        self.move = move            # The move that led to this node
        self.wins = 0               # Wins recorded through this node
        self.visits = 0             # Times this node has been visited
        self.children = []          # Expanded child nodes
        # Store unexplored moves so we expand one at a time
        self.untried_moves = bfs_get_valid_moves(board, color)

    def is_fully_expanded(self):
        """True when all valid moves from this node have been expanded."""
        return len(self.untried_moves) == 0

    def is_terminal(self):
        """True when the game is over at this node."""
        return is_game_over(self.board)

    def ucb1_score(self, exploration=UCB1_C):
        """
        UCB1 formula: balances exploitation (high win rate) and
        exploration (less-visited nodes).
        Score = (wins/visits) + C * sqrt(ln(parent_visits) / visits)
        """
        if self.visits == 0:
            return float('inf')  # Unvisited nodes are always explored first
        exploitation = self.wins / self.visits
        exploration_term = exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        return exploitation + exploration_term

    def best_child(self):
        """Return the child with the highest UCB1 score."""
        return max(self.children, key=lambda n: n.ucb1_score())

    def most_visited_child(self):
        """
        Return the child visited most often.
        Used to pick the final move after all simulations are complete.
        """
        return max(self.children, key=lambda n: n.visits)


def _select(node):
    """
    Step 1 – Selection.
    Walk down the tree from the root, always choosing the child with the
    best UCB1 score, until we reach a node that is not fully expanded
    or is a terminal node.
    """
    while not node.is_terminal() and node.is_fully_expanded():
        node = node.best_child()
    return node


def _expand(node):
    """
    Step 2 – Expansion.
    Pick one untried move, create a new child node for it, and add it
    to the tree. Returns the new child node.
    """
    move = node.untried_moves.pop()  # pick an untried move
    new_board = node.board.copy()
    apply_move(new_board, move[0], move[1], node.color)

    # Determine the next player's color
    opp = WHITE if node.color == BLACK else BLACK
    if has_valid_moves(new_board, opp):
        next_color = opp
    elif has_valid_moves(new_board, node.color):
        next_color = node.color  # opponent must pass
    else:
        next_color = opp  # game is over; color doesn't matter

    child = MCTSNode(new_board, next_color, parent=node, move=move)
    node.children.append(child)
    return child


def _heuristic_choice(moves):
    """
    Pick a move from `moves` using the positional weight table as a
    probability distribution — higher-weight cells are chosen more often.
    This is the heuristic rollout policy: it biases simulations toward
    strategically valuable positions without doing a full tree search.
    """
    # Shift all weights to be strictly positive so they can be used as
    # probabilities (the table contains negative values for bad cells).
    weights = [POSITION_WEIGHTS[r][c] + 41 for (r, c) in moves]  # min weight is -40
    total = sum(weights)
    pick = random.uniform(0, total)
    cumulative = 0
    for move, w in zip(moves, weights):
        cumulative += w
        if cumulative >= pick:
            return move
    return moves[-1]  # fallback


def _simulate(node, ai_color):
    """
    Step 3 – Simulation (Playout).
    From the given node, play a heuristic-guided game to the end.
    Returns 1 if `ai_color` wins, 0 otherwise.

    Instead of picking moves at random, each simulated move is sampled
    proportionally to the positional heuristic weight — corners and edges
    are preferred over weak interior or corner-adjacent cells.  This is
    called a "heuristic rollout policy" and makes simulations much more
    informative than pure random play.

    Note: BFS is used in Selection and Expansion for academic correctness.
    Here we use get_valid_moves directly for speed — the hot loop runs
    many times per decision so the BFS queue overhead adds up.
    """
    board = node.board.copy()
    current_color = node.color
    opp = WHITE if ai_color == BLACK else BLACK

    while not is_game_over(board):
        moves = get_valid_moves(board, current_color)  # fast direct lookup
        if moves:
            move = _heuristic_choice(moves)  # heuristic-guided, not purely random
            apply_move(board, move[0], move[1], current_color)
        # Switch turn
        next_color = WHITE if current_color == BLACK else BLACK
        if has_valid_moves(board, next_color):
            current_color = next_color
        elif not has_valid_moves(board, current_color):
            break  # neither can move

    # Determine winner from final board state
    scores = board.get_scores()
    if scores[ai_color] > scores[opp]:
        return 1  # win
    return 0  # loss


def _backpropagate(node, result):
    """
    Step 4 – Backpropagation.
    Walk back up the tree from the expanded node to the root,
    updating every node's visit count and win count.
    """
    while node is not None:
        node.visits += 1
        node.wins += result
        node = node.parent


def mcts_get_best_move(board, color, simulations=SIMULATIONS):
    """
    Run MCTS for `simulations` iterations and return the best move (row, col).
    Returns None if there are no valid moves.
    """
    valid_moves = bfs_get_valid_moves(board, color)
    if not valid_moves:
        return None

    # Create the root node for the current board state
    root = MCTSNode(board.copy(), color)

    for _ in range(simulations):
        # Step 1: Selection
        node = _select(root)

        # Step 2: Expansion (if not terminal and has untried moves)
        if not node.is_terminal() and not node.is_fully_expanded():
            node = _expand(node)

        # Step 3: Simulation
        result = _simulate(node, color)

        # Step 4: Backpropagation
        _backpropagate(node, result)

    # After all simulations, pick the most-visited child as the best move
    if not root.children:
        return random.choice(valid_moves)

    best = root.most_visited_child()
    return best.move
