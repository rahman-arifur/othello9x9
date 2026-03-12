# game/game_manager.py
# Controls the game loop: turn switching, move application, game-over detection.

from game.board import Board, BLACK, WHITE
from game.rules import (get_valid_moves, apply_move, is_game_over,
                        get_winner, has_valid_moves)


class GameManager:
    """
    Manages one game session.
    Holds the board, the two players (AI or Human), and whose turn it is.
    """

    def __init__(self, player_black, player_white):
        """
        player_black: an AI or HumanPlayer instance that plays as BLACK.
        player_white: an AI or HumanPlayer instance that plays as WHITE.
        Black always goes first in Othello.
        """
        self.board = Board()
        self.player_black = player_black
        self.player_white = player_white
        self.current_color = BLACK  # Black goes first
        self.game_over = False
        self.winner = None
        self.move_history = []  # list of (color, row, col) tuples

    def get_current_player(self):
        """Return the player object whose turn it currently is."""
        if self.current_color == BLACK:
            return self.player_black
        return self.player_white

    def get_valid_moves_for_current(self):
        """Return valid moves for the current player."""
        return get_valid_moves(self.board, self.current_color)

    def apply_move(self, row, col):
        """
        Apply a move at (row, col) for the current player.
        Returns True if successful, False if illegal.
        """
        valid = get_valid_moves(self.board, self.current_color)
        if (row, col) not in valid:
            return False
        apply_move(self.board, row, col, self.current_color)
        self.move_history.append((self.current_color, row, col))
        self._switch_turn()
        return True

    def _switch_turn(self):
        """
        Switch to the opponent's turn.
        If the opponent has no moves, pass back to current player.
        If neither player can move, the game is over.
        """
        next_color = WHITE if self.current_color == BLACK else BLACK

        if has_valid_moves(self.board, next_color):
            self.current_color = next_color
        elif has_valid_moves(self.board, self.current_color):
            # Opponent must pass; current player goes again
            pass  # current_color stays the same
        else:
            # Neither player can move — game over
            self._end_game()

        if is_game_over(self.board):
            self._end_game()

    def _end_game(self):
        """Mark the game as finished and determine the winner."""
        self.game_over = True
        self.winner = get_winner(self.board)

    def get_state(self):
        """
        Return a JSON-serialisable snapshot of the current game state.
        Used by the Flask app to send data to the browser.
        """
        scores = self.board.get_scores()
        # Last move: the most recent (color, row, col) entry in history
        last = self.move_history[-1] if self.move_history else None
        return {
            "board": self.board.grid,         # 9x9 list of 0/1/2
            "current_color": self.current_color,
            "game_over": self.game_over,
            "winner": self.winner,
            "scores": {
                "black": scores[BLACK],
                "white": scores[WHITE],
            },
            "valid_moves": self.get_valid_moves_for_current() if not self.game_over else [],
            "last_move": [last[1], last[2]] if last else None,  # [row, col]
            "last_move_color": last[0] if last else None,
        }
