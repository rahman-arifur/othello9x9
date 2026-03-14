# ui/app.py
# Flask web server. Manages game sessions and exposes all API endpoints
# that the browser calls via JavaScript.

import threading
from flask import Flask, render_template, request, jsonify, session
from game.board import BLACK, WHITE
from game.game_manager import GameManager
from ai.white_ai import WhiteAI
from ai.black_ai import BlackAI
from ai.human_player import HumanPlayer

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="../static",
)
app.secret_key = "othello-ai-2v2-secret"  # required for Flask session

# --- Global game state ---
# We store the active GameManager and a lock for thread safety.
# In a production app you'd use a proper session store, but for this
# educational project a single global instance is fine.
game_manager = None
game_lock = threading.Lock()

# Store the game mode and AI delay separately so JS can read them
game_config = {
    "mode": None,          # "ai_vs_ai" | "human_vs_ai1" | "human_vs_ai2"
    "human_color": None,   # BLACK or WHITE (only in human modes)
    "delay": 2.0,          # seconds between AI moves
}


def _build_game(mode, human_color, delay):
    """
    Factory: create the correct GameManager for the chosen mode.
    Returns (game_manager, game_config_dict).
    """
    delay = max(0.5, min(5.0, float(delay)))  # clamp to 0.5–5.0 s

    if mode == "ai_vs_ai":
        black_player = BlackAI(BLACK)
        white_player = WhiteAI(WHITE)

    elif mode == "human_vs_ai1":
        # Human vs White AI (AI1)
        if human_color == BLACK:
            black_player = HumanPlayer(BLACK)
            white_player = WhiteAI(WHITE)
        else:
            black_player = BlackAI(BLACK)   # AI2 fills the other slot
            white_player = HumanPlayer(WHITE)

    elif mode == "human_vs_ai2":
        # Human vs Black AI (AI2)
        if human_color == BLACK:
            black_player = HumanPlayer(BLACK)
            white_player = WhiteAI(WHITE)   # AI1 fills the other slot
        else:
            black_player = BlackAI(BLACK)
            white_player = HumanPlayer(WHITE)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    gm = GameManager(black_player, white_player)
    cfg = {"mode": mode, "human_color": human_color, "delay": delay}
    return gm, cfg


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def menu():
    """Serve the main menu page."""
    return render_template("menu.html")


@app.route("/game")
def game_page():
    """Serve the game board page."""
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def api_start():
    """
    Start a new game.
    Expects JSON body:
      { "mode": "ai_vs_ai"|"human_vs_ai1"|"human_vs_ai2",
        "human_color": 1|2,   (only needed for human modes)
        "delay": 0.5–5.0 }
    """
    global game_manager, game_config
    data = request.get_json()

    mode = data.get("mode", "ai_vs_ai")
    human_color = int(data.get("human_color", BLACK))
    delay = float(data.get("delay", 2.0))

    with game_lock:
        game_manager, game_config = _build_game(mode, human_color, delay)

    state = game_manager.get_state()
    state["config"] = game_config
    return jsonify(state)


@app.route("/api/state", methods=["GET"])
def api_state():
    """
    Return the current game state as JSON.
    Called by the browser repeatedly (polling) to update the board display.
    """
    if game_manager is None:
        return jsonify({"error": "No game in progress"}), 400

    state = game_manager.get_state()
    state["config"] = game_config
    return jsonify(state)


@app.route("/api/ai_move", methods=["POST"])
def api_ai_move():
    """
    Trigger the current AI player to make one move.
    The browser calls this endpoint when it is the AI's turn.
    Returns the updated game state.
    """
    if game_manager is None:
        return jsonify({"error": "No game in progress"}), 400

    with game_lock:
        if game_manager.game_over:
            return jsonify(game_manager.get_state())

        current_player = game_manager.get_current_player()

        # Only proceed if this is an AI player (not HumanPlayer)
        if isinstance(current_player, HumanPlayer):
            state = game_manager.get_state()
            state["config"] = game_config
            return jsonify(state)

        move = current_player.choose_move(game_manager.board)
        if move:
            game_manager.apply_move(move[0], move[1])

    state = game_manager.get_state()
    state["config"] = game_config
    return jsonify(state)


@app.route("/api/human_move", methods=["POST"])
def api_human_move():
    """
    Student 2 responsibility — backend human move processing.
    Receive a human move click from the browser, validate it, and apply it.
    Expects JSON body: { "row": int, "col": int }
    Returns the updated game state or an error if the move is invalid.
    """
    if game_manager is None:
        return jsonify({"error": "No game in progress"}), 400

    data = request.get_json()
    row = int(data.get("row", -1))
    col = int(data.get("col", -1))

    with game_lock:
        if game_manager.game_over:
            state = game_manager.get_state()
            state["config"] = game_config
            return jsonify(state)

        current_player = game_manager.get_current_player()

        # Only accept clicks when it is actually a human's turn
        if not isinstance(current_player, HumanPlayer):
            return jsonify({"error": "Not the human's turn"}), 400

        # Validate and apply the move via HumanPlayer.submit_move
        accepted = current_player.submit_move(row, col, game_manager.board)
        if not accepted:
            return jsonify({"error": "Invalid move"}), 400

        # Retrieve the move from HumanPlayer and apply it to the game
        move = current_player.choose_move(game_manager.board)
        if move:
            game_manager.apply_move(move[0], move[1])

    state = game_manager.get_state()
    state["config"] = game_config
    return jsonify(state)


@app.route("/api/restart", methods=["POST"])
def api_restart():
    """
    Restart the game with the same settings.
    """
    global game_manager
    if game_manager is None or game_config["mode"] is None:
        return jsonify({"error": "No game to restart"}), 400

    with game_lock:
        game_manager, _ = _build_game(
            game_config["mode"],
            game_config["human_color"],
            game_config["delay"],
        )

    state = game_manager.get_state()
    state["config"] = game_config
    return jsonify(state)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
