

import sys
import os

# If a local virtual environment exists at `./.venv`, re-exec this
# script with the venv's Python so the user can simply run:
#   python main.py
# even when their system Python is a distinct, managed install.
proj_root = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(proj_root, ".venv", "bin", "python")

# If we're not already running under the project's venv, and the venv
# exists, replace the current process with the venv Python.
try:
    running_in_venv = os.path.commonpath([sys.executable, os.path.join(proj_root, ".venv")]) == os.path.join(proj_root, ".venv")
except Exception:
    running_in_venv = False

if os.path.exists(venv_python) and not running_in_venv:
    os.execv(venv_python, [venv_python] + sys.argv)

# Make sure all sub-packages can be imported from the project root
sys.path.insert(0, proj_root)

from ui.app import app


if __name__ == "__main__":
    print("=" * 50)
    print("  Othello AI Battle — 9x9 Board")
    print("  Open your browser at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=False, port=5000)
