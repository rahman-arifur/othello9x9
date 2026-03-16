# Othello 9x9 AI Battle

Web-based 9x9 Othello/Reversi project built with Flask.

This project supports:
- AI vs AI matches
- Human vs AI1
- Human vs AI2

The two AI agents use different strategies:
- AI1 (White): Minimax with Alpha-Beta pruning + heuristic + fuzzy logic
- AI2 (Black): MCTS with BFS-based move generation

## Features

- 9x9 Othello board with turn-by-turn updates
- Browser UI with menu, mode selection, and restart
- Configurable AI delay (0.5 to 5.0 seconds)
- Human move validation on server side
- Last-move highlighting and live score display

## Tech Stack

- Python 3
- Flask
- HTML/CSS/JavaScript (vanilla)

## Project Structure

```text
othello9x9/
	ai/
		base_ai.py          # Shared AI interface
		white_ai.py         # AI1: Minimax + heuristic + fuzzy logic
		black_ai.py         # AI2: MCTS + BFS move generation
		human_player.py     # Human input adapter
	algorithms/
		minimax.py
		mcts.py
		bfs_search.py
		heuristic.py
		fuzzy_logic.py
	game/
		board.py            # 9x9 board model
		rules.py            # Move legality + flipping rules
		game_manager.py     # Turn flow, state snapshots, game over
	ui/
		app.py              # Flask app and API endpoints
		templates/
			menu.html
			index.html
	static/
		style.css
	requirements.txt
	main.py               # Currently empty/not used
```

## Setup

1. Clone the repository and open it.
2. Create a virtual environment.
3. Install dependencies.

Example (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Example (Windows PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

Start the Flask server:

```bash
python ui/app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Gameplay Modes

- `ai_vs_ai`: AI1 (White) vs AI2 (Black)
- `human_vs_ai1`: Human plays against AI1
- `human_vs_ai2`: Human plays against AI2

In human modes, the player chooses color from the menu.

## AI Overview

### AI1 (White)

- Search: Minimax with Alpha-Beta pruning (`algorithms/minimax.py`)
- Evaluation: weighted blend of:
	- positional heuristic (`algorithms/heuristic.py`)
	- fuzzy evaluation (`algorithms/fuzzy_logic.py`)

### AI2 (Black)

- Search: Monte Carlo Tree Search (`algorithms/mcts.py`)
- Move generation: BFS-based legal move listing (`algorithms/bfs_search.py`)
- Rollouts: heuristic-guided random playouts using position weights

## API Endpoints

All endpoints are served by `ui/app.py`.

- `GET /` -> menu page
- `GET /game` -> game board page
- `POST /api/start` -> start a new game with mode/config
- `GET /api/state` -> fetch current game state
- `POST /api/ai_move` -> execute one AI turn
- `POST /api/human_move` -> submit human move `{row, col}`
- `POST /api/restart` -> restart with same config

