# Adversarial Search: Minimax algorithm with Alpha-Beta pruning.
#
# Minimax simulates the game tree: the AI tries to maximise its own score
# while assuming the opponent will try to minimise it.
# Alpha-Beta pruning cuts off branches that can't affect the final decision,
# making the search significantly faster without changing the result.

from game.board import BLACK, WHITE
from game.rules import get_valid_moves, apply_move, is_game_over, has_valid_moves
from algorithms.heuristic import evaluate_board
from algorithms.fuzzy_logic import fuzzy_evaluate_board

# How many moves ahead the AI looks (search depth).
# Higher = smarter but slower. 4 is a good beginner-friendly balance.
DEFAULT_DEPTH = 4


def combined_evaluate(board, color):
    """
    Combine heuristic positional scoring and fuzzy logic into one score.
    Weighted sum: 60% heuristic + 40% fuzzy.
    """
    heuristic_score = evaluate_board(board, color)
    fuzzy_score = fuzzy_evaluate_board(board, color)
    return 0.6 * heuristic_score + 0.4 * fuzzy_score


def minimax(board, depth, alpha, beta, maximizing, ai_color):
    """
    Minimax with Alpha-Beta pruning.

    Parameters:
      board       : current Board object
      depth       : how many more levels to explore
      alpha       : best score the maximizing player can guarantee (starts at -inf)
      beta        : best score the minimizing player can guarantee (starts at +inf)
      maximizing  : True if it's the AI's turn to maximise, False if minimising
      ai_color    : the color the AI is playing as (used for evaluation)

    Returns the best score found from this board state.
    """
    opp_color = WHITE if ai_color == BLACK else BLACK

    # --- Base cases ---
    if depth == 0 or is_game_over(board):
        return combined_evaluate(board, ai_color)

    current_color = ai_color if maximizing else opp_color
    moves = get_valid_moves(board, current_color)

    # If the current player has no moves, they must pass
    if not moves:
        if has_valid_moves(board, opp_color if maximizing else ai_color):
            # Pass turn: flip maximizing flag but keep the same depth
            return minimax(board, depth, alpha, beta, not maximizing, ai_color)
        else:
            # Neither player can move — game over
            return combined_evaluate(board, ai_color)

    if maximizing:
        # AI's turn: try to get the highest score
        best_score = float('-inf')
        for (r, c) in moves:
            # Simulate the move on a copy of the board
            board_copy = board.copy()
            apply_move(board_copy, r, c, current_color)
            score = minimax(board_copy, depth - 1, alpha, beta, False, ai_color)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cut-off: opponent won't allow this branch
        return best_score
    else:
        # Opponent's turn: try to get the lowest score (worst for AI)
        best_score = float('inf')
        for (r, c) in moves:
            board_copy = board.copy()
            apply_move(board_copy, r, c, current_color)
            score = minimax(board_copy, depth - 1, alpha, beta, True, ai_color)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cut-off: AI won't allow this branch
        return best_score


def get_best_move(board, color, depth=DEFAULT_DEPTH):
    """
    Find and return the best move (row, col) for `color` using Minimax.
    Tries every valid move, runs minimax on each, picks the highest scoring one.
    """
    moves = get_valid_moves(board, color)
    if not moves:
        return None

    best_move = None
    best_score = float('-inf')

    for (r, c) in moves:
        board_copy = board.copy()
        apply_move(board_copy, r, c, color)
        # After the AI moves, it's the opponent's turn (minimizing=False)
        score = minimax(board_copy, depth - 1, float('-inf'), float('inf'), False, color)
        if score > best_score:
            best_score = score
            best_move = (r, c)

    return best_move
